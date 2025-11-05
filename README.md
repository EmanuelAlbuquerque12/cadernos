# Baixador de Cadernos do PJe

Baixador automatizado de cadernos (Editais e Diários Eletrônicos) de todos os tribunais brasileiros do sistema PJe.

## 🌐 Aplicação Web Disponível!

**NOVO:** Agora com interface web completa! Use o navegador para baixar e buscar nos cadernos.

```bash
python app.py
# Acesse: http://localhost:5000
```

**Recursos da aplicação web:**
- 📥 Interface gráfica para download
- 🔍 Busca textual nos documentos baixados
- 📊 Estatísticas em tempo real
- 💾 Configuração de pasta de salvamento
- ⚡ Evita downloads duplicados automaticamente

👉 **[Veja a documentação completa da aplicação web](README_WEB.md)**

---

## Características (Linha de Comando)

- Download automatizado de Editais (E) e Diários Eletrônicos (D)
- Suporte a todos os tribunais brasileiros (Nacional, Estaduais e Regionais)
- Downloads paralelos para melhor performance
- Retry automático em caso de falhas
- Organização automática dos arquivos por tribunal/ano/mês
- Logging detalhado de todas as operações
- Relatórios em JSON
- Filtragem por tribunal, data e tipo de caderno

## Requisitos

- Python 3.6 ou superior
- Acesso à internet (conexão do Brasil recomendada)
- Bibliotecas Python: requests, urllib3

**Importante:** A API do PJe pode ter restrições geográficas implementadas via CloudFront. Se você receber erros 403, certifique-se de que está executando o script de um servidor/conexão no Brasil.

## Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd cadernos

# Instale as dependências
pip install -r requirements.txt
```

## Uso Básico

```bash
# Baixar cadernos de hoje de todos os tribunais
python baixador_cadernos.py

# Baixar de uma data específica
python baixador_cadernos.py --data 05/11/2025

# Baixar de um período
python baixador_cadernos.py --data-inicio 01/11/2025 --data-fim 05/11/2025

# Baixar apenas Editais
python baixador_cadernos.py --tipo E

# Baixar apenas Diários Eletrônicos
python baixador_cadernos.py --tipo D

# Baixar de tribunais específicos
python baixador_cadernos.py --tribunal TJSP TRF3 STJ

# Combinar filtros
python baixador_cadernos.py --data 05/11/2025 --tipo E --tribunal TJSP
```

## Opções Avançadas

```bash
# Especificar diretório de saída
python baixador_cadernos.py --output meus_cadernos

# Aumentar número de downloads paralelos (padrão: 5)
python baixador_cadernos.py --workers 10

# Modo silencioso (apenas erros)
python baixador_cadernos.py --quiet

# Modo debug (logs detalhados)
python baixador_cadernos.py --debug

# Ver todas as opções
python baixador_cadernos.py --help
```

## Estrutura de Arquivos

Os arquivos baixados são organizados automaticamente:

```
cadernos_baixados/
├── TJSP/
│   ├── 2025/
│   │   ├── 11/
│   │   │   ├── TJSP_05-11-2025_Edital.pdf
│   │   │   └── TJSP_05-11-2025_Diario.pdf
├── TRF3/
│   ├── 2025/
│   │   ├── 11/
│   │   │   ├── TRF3_05-11-2025_Edital.pdf
│   │   │   └── TRF3_05-11-2025_Diario.pdf
└── relatorio.json
```

## Tribunais Suportados

### Nacional
- CJF - Conselho da Justiça Federal
- CNJ - Conselho Nacional de Justiça
- PJeCor - Corregedorias
- SEEU - Sistema Eletrônico de Execução Unificado
- STJ - Superior Tribunal de Justiça
- STM - Superior Tribunal Militar
- TSE - Tribunal Superior Eleitoral
- TST - Tribunal Superior do Trabalho

### Regionais
- TRF1, TRF2, TRF3, TRF4, TRF5, TRF6 - Tribunais Regionais Federais
- TRT1 a TRT24 - Tribunais Regionais do Trabalho
- TRE-* - Tribunais Regionais Eleitorais de todos os estados

### Estaduais
- TJ* - Tribunais de Justiça de todos os estados
- TJDFT - Tribunal de Justiça do Distrito Federal e Territórios
- TJM* - Tribunais de Justiça Militar (MG, RS, SP)

Para ver a lista completa de siglas, consulte o arquivo `tribunais.json`.

## Logs e Relatórios

O programa gera dois tipos de saída:

1. **Log de execução** (`baixador_cadernos.log`): Log detalhado de todas as operações
2. **Relatório JSON** (`cadernos_baixados/relatorio.json`): Relatório estruturado com:
   - Estatísticas gerais
   - Detalhes de cada download
   - Erros encontrados

## Exemplos de Uso

### Baixar cadernos diários automaticamente (cron)

```bash
# Adicione ao crontab para executar todo dia às 8h
0 8 * * * cd /caminho/para/cadernos && python baixador_cadernos.py
```

### Baixar de múltiplos tribunais específicos

```bash
# Tribunais Superiores
python baixador_cadernos.py --tribunal STJ STF TST TSE

# Tribunais de São Paulo
python baixador_cadernos.py --tribunal TJSP TRF3 TRT2 TRT15

# Tribunais Regionais Federais
python baixador_cadernos.py --tribunal TRF1 TRF2 TRF3 TRF4 TRF5 TRF6
```

### Baixar período específico

```bash
# Última semana
python baixador_cadernos.py --data-inicio 29/10/2025 --data-fim 05/11/2025

# Mês completo
python baixador_cadernos.py --data-inicio 01/11/2025 --data-fim 30/11/2025
```

## API do PJe

O programa utiliza a API oficial do PJe:
- **Base URL**: `https://comunicaapi.pje.jus.br/api/v1/caderno`
- **Endpoint**: `/{sigla_tribunal}/{data}/{tipo}`
- **Tipos**:
  - `E` - Edital
  - `D` - Diário Eletrônico
- **Formato de data**: DD-MM-YYYY

## Troubleshooting

### Erro 403 (Forbidden)
- A API do PJe pode estar configurada para aceitar apenas requisições do Brasil
- Verifique se você está executando o script de um servidor/conexão brasileira
- Se estiver usando VPN, tente desconectá-la ou usar uma VPN brasileira

### Erro de conexão
- Verifique sua conexão com a internet
- A API pode estar temporariamente indisponível
- Use `--debug` para ver detalhes do erro

### Cadernos não encontrados
- Nem todos os tribunais publicam cadernos todos os dias
- Verifique se a data é válida (não futura)
- Alguns tribunais podem não ter cadernos disponíveis

### Performance
- Ajuste o número de workers com `--workers` (cuidado para não sobrecarregar a API)
- Use filtros para baixar apenas o necessário

## Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto é disponibilizado sob a licença MIT.

## Avisos

- Este programa acessa dados públicos disponibilizados pelos tribunais
- Respeite os limites de taxa da API
- Use de forma responsável

## Suporte

Para reportar bugs ou sugerir melhorias, abra uma issue no repositório.
