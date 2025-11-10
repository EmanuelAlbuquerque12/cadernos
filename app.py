#!/usr/bin/env python3
"""
Aplicação Web - Baixador e Buscador de Cadernos PJe
"""

import os
import json
import threading
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import baixador_cadernos as bc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pje-cadernos-secret-key'

# Arquivo de configuração
CONFIG_FILE = 'config.json'
INDEX_FILE = 'indice_documentos.json'

# Estado global
download_status = {
    'em_andamento': False,
    'progresso': 0,
    'total': 0,
    'mensagem': ''
}


def carregar_config():
    """Carrega configurações do arquivo"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    # Define C:\Cadernos PJe como padrão (Windows)
    return {
        'pasta_salvamento': r'C:\Cadernos PJe',
        'workers': 10  # Velocidade máxima por padrão
    }


def salvar_config(config):
    """Salva configurações no arquivo"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def carregar_indice():
    """Carrega índice de documentos baixados"""
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'documentos': [], 'ultima_atualizacao': None}


def salvar_indice(indice):
    """Salva índice de documentos"""
    indice['ultima_atualizacao'] = datetime.now().isoformat()
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(indice, f, ensure_ascii=False, indent=2)


def adicionar_ao_indice(arquivo_path, sigla, data, tipo, conteudo_texto=None):
    """Adiciona documento ao índice"""
    indice = carregar_indice()

    # Verifica se já existe
    for doc in indice['documentos']:
        if doc['arquivo'] == str(arquivo_path):
            return

    indice['documentos'].append({
        'arquivo': str(arquivo_path),
        'sigla': sigla,
        'data': data,
        'tipo': tipo,
        'data_download': datetime.now().isoformat(),
        'tamanho': os.path.getsize(arquivo_path) if os.path.exists(arquivo_path) else 0,
        'texto_extraido': conteudo_texto is not None
    })

    salvar_indice(indice)


def documento_ja_baixado(sigla, data, tipo):
    """Verifica se documento já foi baixado"""
    indice = carregar_indice()
    tipo_nome = bc.BaixadorCadernos.TIPOS_CADERNO[tipo]

    for doc in indice['documentos']:
        if (doc['sigla'] == sigla and
            doc['data'] == data and
            doc['tipo'] == tipo):
            # Verifica se arquivo ainda existe
            if os.path.exists(doc['arquivo']):
                return True

    return False


@app.route('/')
def index():
    """Página principal"""
    config = carregar_config()
    tribunais = bc.BaixadorCadernos().carregar_tribunais()
    indice = carregar_indice()

    # Agrupa por UF
    tribunais_por_uf = {}
    for tribunal in tribunais:
        uf = tribunal['uf'] if tribunal['uf'] else 'Nacional'
        if uf not in tribunais_por_uf:
            tribunais_por_uf[uf] = []
        tribunais_por_uf[uf].append(tribunal)

    return render_template('index.html',
                         config=config,
                         tribunais_por_uf=tribunais_por_uf,
                         total_documentos=len(indice['documentos']))


@app.route('/api/selecionar_pasta', methods=['GET'])
def api_selecionar_pasta():
    """API para abrir seletor de pasta nativo do Windows"""
    try:
        import tkinter as tk
        from tkinter import filedialog

        # Cria janela invisível
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)

        # Abre seletor de pasta
        pasta_selecionada = filedialog.askdirectory(
            title='Selecione a pasta para salvar os cadernos',
            initialdir='C:\\'
        )

        root.destroy()

        if pasta_selecionada:
            return jsonify({'sucesso': True, 'pasta': pasta_selecionada})
        else:
            return jsonify({'sucesso': False, 'mensagem': 'Nenhuma pasta selecionada'})

    except Exception as e:
        return jsonify({'sucesso': False, 'erro': str(e)}), 500


@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """API para configurações"""
    if request.method == 'POST':
        data = request.json
        config = carregar_config()

        if 'pasta_salvamento' in data:
            pasta = data['pasta_salvamento']
            # Cria pasta se não existir
            os.makedirs(pasta, exist_ok=True)
            config['pasta_salvamento'] = pasta

        if 'workers' in data:
            config['workers'] = int(data['workers'])

        salvar_config(config)
        return jsonify({'sucesso': True, 'config': config})

    return jsonify(carregar_config())


@app.route('/api/tribunais')
def api_tribunais():
    """API para listar tribunais"""
    baixador = bc.BaixadorCadernos()
    tribunais = baixador.carregar_tribunais()
    return jsonify(tribunais)


@app.route('/api/baixar', methods=['POST'])
def api_baixar():
    """API para iniciar download"""
    global download_status

    if download_status['em_andamento']:
        return jsonify({'erro': 'Já existe um download em andamento'}), 400

    data = request.json
    tribunais_siglas = data.get('tribunais', [])
    data_inicio = data.get('data_inicio')
    data_fim = data.get('data_fim')
    tipos = data.get('tipos', ['E', 'D'])

    if not tribunais_siglas:
        return jsonify({'erro': 'Selecione pelo menos um tribunal'}), 400

    # Inicia download em thread separada
    thread = threading.Thread(
        target=executar_download,
        args=(tribunais_siglas, data_inicio, data_fim, tipos)
    )
    thread.start()

    return jsonify({'sucesso': True, 'mensagem': 'Download iniciado'})


def executar_download(tribunais_siglas, data_inicio, data_fim, tipos):
    """Executa download em background"""
    global download_status

    try:
        download_status['em_andamento'] = True
        download_status['progresso'] = 0
        download_status['mensagem'] = 'Inicializando...'

        config = carregar_config()
        baixador = bc.BaixadorCadernos(
            output_dir=config['pasta_salvamento'],
            max_workers=config['workers']
        )

        # Carrega todos os tribunais
        todos_tribunais = baixador.carregar_tribunais()

        # Filtra tribunais selecionados
        tribunais = [t for t in todos_tribunais
                    if t['sigla'] in tribunais_siglas]

        # Gera lista de datas
        if data_inicio and data_fim:
            data_inicio_fmt = bc.parse_data(data_inicio)
            data_fim_fmt = bc.parse_data(data_fim)
            datas = bc.gerar_lista_datas(data_inicio_fmt, data_fim_fmt)
        else:
            datas = [datetime.now().strftime('%d-%m-%Y')]

        # Filtra downloads já realizados
        tarefas_filtradas = []
        tarefas_puladas = 0

        for tribunal in tribunais:
            for data in datas:
                for tipo in tipos:
                    if documento_ja_baixado(tribunal['sigla'], data, tipo):
                        tarefas_puladas += 1
                    else:
                        tarefas_filtradas.append({
                            'tribunal': tribunal,
                            'data': data,
                            'tipo': tipo
                        })

        total_tarefas = len(tarefas_filtradas)
        download_status['total'] = total_tarefas

        if tarefas_puladas > 0:
            download_status['mensagem'] = f'{tarefas_puladas} documentos já baixados anteriormente'

        if total_tarefas == 0:
            download_status['mensagem'] = 'Todos os documentos já foram baixados'
            download_status['em_andamento'] = False
            return

        # Executa downloads
        download_status['mensagem'] = f'Baixando {total_tarefas} documentos...'

        for i, tarefa in enumerate(tarefas_filtradas):
            resultado = baixador.baixar_caderno(
                tarefa['tribunal']['sigla'],
                tarefa['data'],
                tarefa['tipo'],
                tarefa['tribunal']['nome']
            )

            # Adiciona ao índice se sucesso
            if resultado['sucesso'] and resultado['arquivo']:
                adicionar_ao_indice(
                    resultado['arquivo'],
                    resultado['sigla'],
                    resultado['data'],
                    resultado['tipo']
                )

            download_status['progresso'] = i + 1
            download_status['mensagem'] = f'Baixando {i+1}/{total_tarefas}...'

        # Finaliza
        baixador.salvar_relatorio(
            [{'status': 'concluido'}],
            arquivo='relatorio_web.json'
        )

        download_status['mensagem'] = f'Download concluído! {baixador.stats["sucesso"]} sucessos, {baixador.stats["vazio"]} vazios, {baixador.stats["falha"]} falhas'

    except Exception as e:
        download_status['mensagem'] = f'Erro: {str(e)}'
    finally:
        download_status['em_andamento'] = False


@app.route('/api/status')
def api_status():
    """API para verificar status do download"""
    return jsonify(download_status)


@app.route('/api/buscar', methods=['POST'])
def api_buscar():
    """API para buscar em documentos"""
    data = request.json
    termo = data.get('termo', '').lower().strip()

    if not termo:
        return jsonify({'erro': 'Termo de busca não informado'}), 400

    indice = carregar_indice()
    resultados = []

    for doc in indice['documentos']:
        arquivo_path = doc['arquivo']

        if not os.path.exists(arquivo_path):
            continue

        try:
            # Lê conteúdo do arquivo
            conteudo = None
            extensao = Path(arquivo_path).suffix.lower()

            if extensao == '.html':
                with open(arquivo_path, 'r', encoding='utf-8', errors='ignore') as f:
                    conteudo = f.read().lower()

            elif extensao == '.pdf':
                # Importa PyPDF2 se disponível
                try:
                    import PyPDF2
                    with open(arquivo_path, 'rb') as f:
                        pdf = PyPDF2.PdfReader(f)
                        conteudo = ''
                        for page in pdf.pages:
                            conteudo += page.extract_text().lower()
                except ImportError:
                    # Se PyPDF2 não estiver disponível, pula PDFs
                    continue
                except Exception:
                    continue

            elif extensao == '.xml':
                with open(arquivo_path, 'r', encoding='utf-8', errors='ignore') as f:
                    conteudo = f.read().lower()

            # Busca termo
            if conteudo and termo in conteudo:
                ocorrencias = conteudo.count(termo)
                resultados.append({
                    'arquivo': doc['arquivo'],
                    'sigla': doc['sigla'],
                    'data': doc['data'],
                    'tipo': doc['tipo'],
                    'ocorrencias': ocorrencias,
                    'tamanho': doc['tamanho']
                })

        except Exception as e:
            print(f"Erro ao buscar em {arquivo_path}: {e}")
            continue

    # Ordena por número de ocorrências
    resultados.sort(key=lambda x: x['ocorrencias'], reverse=True)

    return jsonify({
        'termo': termo,
        'total_documentos_analisados': len(indice['documentos']),
        'documentos_encontrados': len(resultados),
        'total_ocorrencias': sum(r['ocorrencias'] for r in resultados),
        'resultados': resultados
    })


@app.route('/api/estatisticas')
def api_estatisticas():
    """API para estatísticas"""
    indice = carregar_indice()
    config = carregar_config()

    # Calcula estatísticas
    total_docs = len(indice['documentos'])
    total_tamanho = sum(doc['tamanho'] for doc in indice['documentos'])

    # Agrupa por tribunal
    por_tribunal = {}
    for doc in indice['documentos']:
        sigla = doc['sigla']
        if sigla not in por_tribunal:
            por_tribunal[sigla] = 0
        por_tribunal[sigla] += 1

    # Agrupa por tipo
    por_tipo = {}
    for doc in indice['documentos']:
        tipo = doc['tipo']
        if tipo not in por_tipo:
            por_tipo[tipo] = 0
        por_tipo[tipo] += 1

    return jsonify({
        'total_documentos': total_docs,
        'tamanho_total_mb': round(total_tamanho / (1024 * 1024), 2),
        'pasta_salvamento': config['pasta_salvamento'],
        'por_tribunal': por_tribunal,
        'por_tipo': por_tipo,
        'ultima_atualizacao': indice['ultima_atualizacao']
    })


def encontrar_porta_disponivel(porta_inicial=5000, max_tentativas=10):
    """Encontra uma porta disponível"""
    import socket
    for porta in range(porta_inicial, porta_inicial + max_tentativas):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', porta))
                return porta
        except OSError:
            continue
    return porta_inicial


def abrir_navegador(porta, delay=1.5):
    """Abre o navegador após um delay"""
    import webbrowser
    import time
    time.sleep(delay)
    webbrowser.open(f'http://localhost:{porta}')


def is_executavel():
    """Detecta se está rodando como executável"""
    import sys
    return getattr(sys, 'frozen', False)


if __name__ == '__main__':
    # Detecta se é executável
    eh_exe = is_executavel()

    # Encontra porta disponível
    porta = encontrar_porta_disponivel()

    print("=" * 60)
    print("📚 Baixador e Buscador de Cadernos PJe")
    print("=" * 60)
    print(f"🌐 Servidor iniciado na porta {porta}")
    print(f"🔗 Acesse: http://localhost:{porta}")
    print("=" * 60)

    if eh_exe:
        print("✨ Abrindo navegador automaticamente...")
        print("⚠️  Não feche esta janela enquanto usar o programa!")

    print("=" * 60)
    print("💡 Pressione Ctrl+C para encerrar")
    print("=" * 60)

    # Abre navegador automaticamente
    if eh_exe:
        thread = threading.Thread(target=abrir_navegador, args=(porta,))
        thread.daemon = True
        thread.start()

    # Inicia servidor
    try:
        # Modo produção para .exe, debug para desenvolvimento
        app.run(
            debug=not eh_exe,
            host='0.0.0.0',
            port=porta,
            use_reloader=False  # Desabilita reloader para evitar problemas com .exe
        )
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("👋 Servidor encerrado. Até logo!")
        print("=" * 60)
