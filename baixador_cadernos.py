#!/usr/bin/env python3
"""
Baixador automatizado de cadernos do PJe
Baixa Editais (E) e Diários Eletrônicos (D) de todos os tribunais brasileiros
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('baixador_cadernos.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class BaixadorCadernos:
    """Baixador de cadernos do PJe"""

    BASE_URL = "https://comunicaapi.pje.jus.br/api/v1/caderno"
    TIPOS_CADERNO = {
        'E': 'Edital',
        'D': 'Diario'
    }

    def __init__(self, output_dir: str = "cadernos_baixados", max_workers: int = 5):
        """
        Inicializa o baixador

        Args:
            output_dir: Diretório onde os cadernos serão salvos
            max_workers: Número máximo de threads paralelas
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.max_workers = max_workers
        self.session = self._create_session()

        # Estatísticas
        self.stats = {
            'total': 0,
            'sucesso': 0,
            'falha': 0,
            'vazio': 0
        }

    def _create_session(self) -> requests.Session:
        """Cria sessão HTTP com retry automático"""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def carregar_tribunais(self, arquivo: str = "tribunais.json") -> List[Dict]:
        """Carrega lista de tribunais do arquivo JSON"""
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            tribunais = []
            for estado in dados:
                for instituicao in estado['instituicoes']:
                    tribunais.append({
                        'sigla': instituicao['sigla'],
                        'nome': instituicao['nome'],
                        'uf': estado['uf'],
                        'estado': estado['nomeEstado']
                    })

            logger.info(f"Carregados {len(tribunais)} tribunais")
            return tribunais

        except FileNotFoundError:
            logger.error(f"Arquivo {arquivo} não encontrado")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON: {e}")
            sys.exit(1)

    def baixar_caderno(self, sigla: str, data: str, tipo: str, nome_tribunal: str) -> Dict:
        """
        Baixa um caderno específico

        Args:
            sigla: Sigla do tribunal
            data: Data no formato DD-MM-YYYY
            tipo: Tipo do caderno (E ou D)
            nome_tribunal: Nome do tribunal para logs

        Returns:
            Dicionário com resultado da operação
        """
        url = f"{self.BASE_URL}/{sigla}/{data}/{tipo}"
        tipo_nome = self.TIPOS_CADERNO[tipo]

        resultado = {
            'sigla': sigla,
            'nome': nome_tribunal,
            'data': data,
            'tipo': tipo,
            'tipo_nome': tipo_nome,
            'sucesso': False,
            'arquivo': None,
            'erro': None
        }

        try:
            logger.debug(f"Baixando {tipo_nome} de {sigla} - {data}")
            response = self.session.get(url, timeout=30)

            if response.status_code == 200:
                # Verifica se há conteúdo
                if not response.content or len(response.content) < 100:
                    logger.debug(f"Caderno vazio: {sigla} - {tipo_nome} - {data}")
                    resultado['erro'] = 'vazio'
                    self.stats['vazio'] += 1
                    return resultado

                # Salva o arquivo
                arquivo_path = self._salvar_arquivo(
                    sigla, data, tipo, response.content, response.headers
                )

                resultado['sucesso'] = True
                resultado['arquivo'] = str(arquivo_path)
                self.stats['sucesso'] += 1

                logger.info(f"✓ Baixado: {sigla} - {tipo_nome} - {data} ({len(response.content)} bytes)")

            elif response.status_code == 404:
                logger.debug(f"Não encontrado: {sigla} - {tipo_nome} - {data}")
                resultado['erro'] = 'nao_encontrado'
                self.stats['vazio'] += 1

            else:
                logger.warning(f"Erro HTTP {response.status_code}: {sigla} - {tipo_nome} - {data}")
                resultado['erro'] = f'http_{response.status_code}'
                self.stats['falha'] += 1

        except requests.exceptions.Timeout:
            logger.warning(f"Timeout: {sigla} - {tipo_nome} - {data}")
            resultado['erro'] = 'timeout'
            self.stats['falha'] += 1

        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de requisição: {sigla} - {tipo_nome} - {data}: {e}")
            resultado['erro'] = str(e)
            self.stats['falha'] += 1

        except Exception as e:
            logger.error(f"Erro inesperado: {sigla} - {tipo_nome} - {data}: {e}")
            resultado['erro'] = str(e)
            self.stats['falha'] += 1

        return resultado

    def _salvar_arquivo(self, sigla: str, data: str, tipo: str, conteudo: bytes,
                       headers: Dict) -> Path:
        """Salva o arquivo baixado com estrutura organizada"""
        # Determina extensão baseada no content-type
        content_type = headers.get('Content-Type', '')
        if 'pdf' in content_type.lower():
            extensao = 'pdf'
        elif 'html' in content_type.lower():
            extensao = 'html'
        elif 'xml' in content_type.lower():
            extensao = 'xml'
        else:
            extensao = 'dat'

        # Cria estrutura de diretórios: sigla/ano/mes/
        data_parts = data.split('-')
        ano, mes = data_parts[2], data_parts[1]

        dir_tribunal = self.output_dir / sigla / ano / mes
        dir_tribunal.mkdir(parents=True, exist_ok=True)

        # Nome do arquivo: SIGLA_DATA_TIPO.extensao
        tipo_nome = self.TIPOS_CADERNO[tipo]
        nome_arquivo = f"{sigla}_{data}_{tipo_nome}.{extensao}"
        arquivo_path = dir_tribunal / nome_arquivo

        # Salva o arquivo
        with open(arquivo_path, 'wb') as f:
            f.write(conteudo)

        return arquivo_path

    def baixar_todos(self, tribunais: List[Dict], datas: List[str],
                    tipos: List[str] = None) -> List[Dict]:
        """
        Baixa cadernos de todos os tribunais para as datas especificadas

        Args:
            tribunais: Lista de dicionários com informações dos tribunais
            datas: Lista de datas no formato DD-MM-YYYY
            tipos: Lista de tipos a baixar (default: ['E', 'D'])

        Returns:
            Lista com resultados de todas as operações
        """
        if tipos is None:
            tipos = ['E', 'D']

        # Cria lista de tarefas
        tarefas = []
        for tribunal in tribunais:
            for data in datas:
                for tipo in tipos:
                    tarefas.append({
                        'sigla': tribunal['sigla'],
                        'nome': tribunal['nome'],
                        'data': data,
                        'tipo': tipo
                    })

        self.stats['total'] = len(tarefas)
        logger.info(f"Iniciando download de {len(tarefas)} cadernos...")
        logger.info(f"Tribunais: {len(tribunais)}, Datas: {len(datas)}, Tipos: {len(tipos)}")

        resultados = []

        # Executa downloads em paralelo
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(
                    self.baixar_caderno,
                    tarefa['sigla'],
                    tarefa['data'],
                    tarefa['tipo'],
                    tarefa['nome']
                ): tarefa
                for tarefa in tarefas
            }

            # Processa resultados conforme completam
            for i, future in enumerate(as_completed(futures), 1):
                resultado = future.result()
                resultados.append(resultado)

                # Log de progresso a cada 10%
                if i % max(1, len(tarefas) // 10) == 0:
                    progresso = (i / len(tarefas)) * 100
                    logger.info(f"Progresso: {progresso:.1f}% ({i}/{len(tarefas)})")

        return resultados

    def exibir_estatisticas(self):
        """Exibe estatísticas finais do download"""
        logger.info("=" * 60)
        logger.info("ESTATÍSTICAS FINAIS")
        logger.info("=" * 60)
        logger.info(f"Total de tentativas: {self.stats['total']}")
        logger.info(f"Sucesso: {self.stats['sucesso']} ({self.stats['sucesso']/max(1, self.stats['total'])*100:.1f}%)")
        logger.info(f"Vazios/Não encontrados: {self.stats['vazio']}")
        logger.info(f"Falhas: {self.stats['falha']}")
        logger.info("=" * 60)

    def salvar_relatorio(self, resultados: List[Dict], arquivo: str = "relatorio.json"):
        """Salva relatório detalhado em JSON"""
        relatorio_path = self.output_dir / arquivo
        with open(relatorio_path, 'w', encoding='utf-8') as f:
            json.dump({
                'data_execucao': datetime.now().isoformat(),
                'estatisticas': self.stats,
                'resultados': resultados
            }, f, ensure_ascii=False, indent=2)

        logger.info(f"Relatório salvo em: {relatorio_path}")


def parse_data(data_str: str) -> str:
    """
    Converte data para o formato esperado pela API (DD-MM-YYYY)

    Args:
        data_str: Data em formato DD/MM/YYYY ou DD-MM-YYYY ou YYYY-MM-DD

    Returns:
        Data no formato DD-MM-YYYY
    """
    # Remove espaços
    data_str = data_str.strip()

    # Tenta diferentes formatos
    formatos = ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']

    for formato in formatos:
        try:
            data_obj = datetime.strptime(data_str, formato)
            return data_obj.strftime('%d-%m-%Y')
        except ValueError:
            continue

    raise ValueError(f"Formato de data inválido: {data_str}")


def gerar_lista_datas(data_inicio: str, data_fim: str) -> List[str]:
    """
    Gera lista de datas entre data_inicio e data_fim

    Args:
        data_inicio: Data inicial (DD-MM-YYYY)
        data_fim: Data final (DD-MM-YYYY)

    Returns:
        Lista de datas no formato DD-MM-YYYY
    """
    inicio = datetime.strptime(data_inicio, '%d-%m-%Y')
    fim = datetime.strptime(data_fim, '%d-%m-%Y')

    datas = []
    data_atual = inicio
    while data_atual <= fim:
        datas.append(data_atual.strftime('%d-%m-%Y'))
        data_atual += timedelta(days=1)

    return datas


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Baixador automatizado de cadernos do PJe',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  # Baixar cadernos de hoje de todos os tribunais
  python baixador_cadernos.py

  # Baixar de uma data específica
  python baixador_cadernos.py --data 05/11/2025

  # Baixar de um período
  python baixador_cadernos.py --data-inicio 01/11/2025 --data-fim 05/11/2025

  # Baixar apenas Editais
  python baixador_cadernos.py --tipo E

  # Baixar de tribunais específicos
  python baixador_cadernos.py --tribunal TJSP TRF3 STJ

  # Modo silencioso (apenas erros)
  python baixador_cadernos.py --quiet

  # Debug detalhado
  python baixador_cadernos.py --debug
        """
    )

    parser.add_argument(
        '--data',
        type=str,
        help='Data para download (formato: DD/MM/YYYY). Padrão: hoje'
    )

    parser.add_argument(
        '--data-inicio',
        type=str,
        help='Data inicial para período de download (formato: DD/MM/YYYY)'
    )

    parser.add_argument(
        '--data-fim',
        type=str,
        help='Data final para período de download (formato: DD/MM/YYYY)'
    )

    parser.add_argument(
        '--tipo',
        type=str,
        nargs='+',
        choices=['E', 'D'],
        default=['E', 'D'],
        help='Tipos de caderno a baixar: E (Edital) e/ou D (Diário)'
    )

    parser.add_argument(
        '--tribunal',
        type=str,
        nargs='+',
        help='Siglas de tribunais específicos (ex: TJSP TRF3 STJ)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='cadernos_baixados',
        help='Diretório de saída (padrão: cadernos_baixados)'
    )

    parser.add_argument(
        '--workers',
        type=int,
        default=5,
        help='Número de downloads paralelos (padrão: 5)'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Modo silencioso (apenas erros)'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Modo debug (logs detalhados)'
    )

    args = parser.parse_args()

    # Configura nível de log
    if args.quiet:
        logger.setLevel(logging.ERROR)
    elif args.debug:
        logger.setLevel(logging.DEBUG)

    # Determina datas
    if args.data_inicio and args.data_fim:
        data_inicio = parse_data(args.data_inicio)
        data_fim = parse_data(args.data_fim)
        datas = gerar_lista_datas(data_inicio, data_fim)
        logger.info(f"Baixando período: {data_inicio} a {data_fim} ({len(datas)} dias)")
    elif args.data:
        datas = [parse_data(args.data)]
        logger.info(f"Baixando data: {datas[0]}")
    else:
        # Usa data de hoje
        datas = [datetime.now().strftime('%d-%m-%Y')]
        logger.info(f"Baixando data de hoje: {datas[0]}")

    # Inicializa baixador
    baixador = BaixadorCadernos(output_dir=args.output, max_workers=args.workers)

    # Carrega tribunais
    todos_tribunais = baixador.carregar_tribunais()

    # Filtra tribunais se especificado
    if args.tribunal:
        siglas_upper = [s.upper() for s in args.tribunal]
        tribunais = [t for t in todos_tribunais if t['sigla'].upper() in siglas_upper]
        if not tribunais:
            logger.error(f"Nenhum tribunal encontrado com as siglas: {args.tribunal}")
            sys.exit(1)
        logger.info(f"Baixando de {len(tribunais)} tribunais específicos")
    else:
        tribunais = todos_tribunais
        logger.info(f"Baixando de todos os {len(tribunais)} tribunais")

    # Executa downloads
    inicio = time.time()
    resultados = baixador.baixar_todos(tribunais, datas, args.tipo)
    duracao = time.time() - inicio

    # Exibe estatísticas
    baixador.exibir_estatisticas()
    logger.info(f"Tempo total: {duracao:.2f} segundos")

    # Salva relatório
    baixador.salvar_relatorio(resultados)

    logger.info(f"Arquivos salvos em: {baixador.output_dir}")

    return 0 if baixador.stats['falha'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
