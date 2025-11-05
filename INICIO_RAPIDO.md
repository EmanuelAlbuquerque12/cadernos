# Início Rápido - Baixador de Cadernos PJe

## 🌐 RECOMENDADO: Aplicação Web

A forma mais fácil de usar é através da interface web:

```bash
# 1. Clone e entre no diretório
git clone <url-do-repositorio>
cd cadernos

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Inicie a aplicação web
python app.py
# ou
./iniciar_web.sh

# 4. Abra no navegador
# http://localhost:5000
```

**Com a aplicação web você pode:**
- ✨ Interface gráfica amigável
- 📁 Escolher pasta de salvamento
- 🔍 Buscar nos documentos baixados
- 📊 Ver estatísticas
- ⚡ Evita downloads duplicados automaticamente

👉 [Ver documentação completa da web](README_WEB.md)

---

## 💻 Alternativa: Linha de Comando

Se preferir usar pelo terminal:

## Comandos Mais Usados

```bash
# Baixar cadernos de hoje de todos os tribunais
python baixador_cadernos.py

# Baixar de um tribunal específico
python baixador_cadernos.py --tribunal TJSP

# Baixar de múltiplos tribunais
python baixador_cadernos.py --tribunal TJSP TRF3 STJ

# Baixar apenas Editais
python baixador_cadernos.py --tipo E

# Baixar apenas Diários
python baixador_cadernos.py --tipo D

# Baixar de uma data específica
python baixador_cadernos.py --data 05/11/2025

# Baixar de um período
python baixador_cadernos.py --data-inicio 01/11/2025 --data-fim 05/11/2025
```

## Onde os Arquivos São Salvos?

Os arquivos são salvos em `cadernos_baixados/` com a seguinte estrutura:

```
cadernos_baixados/
├── TJSP/2025/11/TJSP_05-11-2025_Edital.pdf
├── TJSP/2025/11/TJSP_05-11-2025_Diario.pdf
└── relatorio.json
```

## Ver Progresso e Logs

- **Durante execução**: Os logs aparecem no terminal
- **Depois**: Verifique o arquivo `baixador_cadernos.log`
- **Relatório**: Veja `cadernos_baixados/relatorio.json`

## Exemplos Práticos

### Download Diário Automatizado
```bash
# Adicione ao crontab para executar todo dia às 8h
0 8 * * * cd /caminho/para/cadernos && python baixador_cadernos.py
```

### Baixar Tribunais de SP
```bash
python baixador_cadernos.py --tribunal TJSP TRF3 TRT2 TRT15
```

### Baixar Tribunais Superiores
```bash
python baixador_cadernos.py --tribunal STJ STF TST TSE CNJ
```

## Problemas Comuns

### Erro 403
A API só funciona no Brasil. Execute de uma conexão brasileira.

### Nenhum arquivo baixado
Nem todos os tribunais publicam cadernos todos os dias. Isso é normal.

### Muito lento
Aumente o número de workers:
```bash
python baixador_cadernos.py --workers 10
```

## Ver Todas as Opções

```bash
python baixador_cadernos.py --help
```

## Lista de Siglas dos Tribunais

Consulte o arquivo `tribunais.json` para ver todas as 115 siglas disponíveis.

Principais:
- **Superiores**: STJ, STF, TST, TSE, STM, CNJ, CJF
- **TRFs**: TRF1, TRF2, TRF3, TRF4, TRF5, TRF6
- **Estaduais**: TJSP, TJRJ, TJMG, TJRS, TJPR, etc.
- **TRTs**: TRT1 a TRT24
- **TREs**: TRE-SP, TRE-RJ, TRE-MG, etc.

## Suporte

Veja a documentação completa em `README.md` ou abra uma issue no repositório.
