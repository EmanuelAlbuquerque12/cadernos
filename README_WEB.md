# 🌐 Aplicação Web - Baixador e Buscador de Cadernos PJe

Interface web completa para baixar e buscar nos cadernos do PJe.

## ✨ Funcionalidades

### 📥 Download de Cadernos
- Interface gráfica amigável para seleção de tribunais
- Escolha personalizada da pasta de salvamento
- Filtros por data, período e tipo (Edital/Diário)
- Downloads paralelos configuráveis
- Barra de progresso em tempo real
- Sistema inteligente que **não baixa documentos duplicados**

### 🔍 Busca nos Documentos
- Busca textual em **todos os documentos já baixados**
- Suporte a PDFs, HTML e XML
- Conta quantas vezes o termo aparece em cada documento
- Não precisa baixar novamente para fazer novas buscas
- Resultados ordenados por relevância (número de ocorrências)

### 📊 Estatísticas
- Total de documentos baixados
- Espaço em disco utilizado
- Documentos por tribunal e tipo
- Top 5 tribunais com mais documentos

## 🚀 Instalação

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd cadernos

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute a aplicação
python app.py
```

A aplicação estará disponível em: **http://localhost:5000**

## 📖 Como Usar

### 1. Primeira Configuração

1. Abra o navegador em `http://localhost:5000`
2. Configure a **pasta de salvamento** onde os arquivos serão salvos
3. Clique em "Salvar Pasta"

### 2. Baixar Cadernos

1. Selecione o **período de datas** (ou deixe em branco para hoje)
2. Escolha os **tipos**: Editais (E) e/ou Diários (D)
3. **Selecione os tribunais**:
   - Use a busca para filtrar tribunais
   - Clique em "Selecionar Todos" ou escolha manualmente
   - Use "Tribunais Superiores" para STJ, STF, TST, etc.
4. Clique em **"Iniciar Download"**
5. Acompanhe o progresso na barra

**Importante:** O sistema lembra o que já foi baixado e **não faz downloads duplicados**!

### 3. Buscar nos Documentos

1. Vá para a aba **"Buscar Documentos"**
2. Digite o termo que deseja procurar
3. Clique em **"Buscar"** ou pressione Enter
4. Veja os resultados com:
   - Número de ocorrências por documento
   - Informações do tribunal e data
   - Caminho completo do arquivo

**Dica:** A busca é feita APENAS nos documentos já baixados. Para buscar em mais documentos, primeiro faça o download na aba "Download".

## 🎯 Recursos Inteligentes

### Evita Downloads Duplicados
O sistema mantém um **índice de todos os documentos baixados** (`indice_documentos.json`). Quando você tenta baixar novamente:
- Verifica se o documento já existe
- Pula documentos duplicados automaticamente
- Mostra quantos documentos foram pulados
- Economiza tempo e banda

### Busca Eficiente
- A busca é feita **localmente** nos arquivos já baixados
- Não precisa conexão com internet
- Resultados instantâneos
- Busque quantas vezes quiser sem reprocessar

### Extração de Texto
- **PDFs**: Usa PyPDF2 para extrair texto
- **HTML/XML**: Lê diretamente o conteúdo
- Busca case-insensitive (não diferencia maiúsculas/minúsculas)
- Conta ocorrências exatas do termo

## 📁 Estrutura de Arquivos

```
cadernos/
├── app.py                      # Servidor Flask
├── baixador_cadernos.py        # Módulo de download
├── tribunais.json              # Lista de tribunais
├── config.json                 # Configurações (gerado automaticamente)
├── indice_documentos.json      # Índice de documentos baixados
├── templates/
│   ├── index.html             # Página de download
│   └── busca.html             # Página de busca
├── static/
│   ├── style.css              # Estilos
│   └── script.js              # JavaScript
└── cadernos_baixados/          # Pasta padrão de downloads
    ├── TJSP/
    │   └── 2025/11/...
    └── relatorio_web.json
```

## ⚙️ Configurações Avançadas

### Alterar Porta
Edite `app.py` linha final:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Mude 5000 para outra porta
```

### Alterar Workers
Na interface web, vá em "Configurações" > "Downloads Paralelos"
- Valor baixo (1-3): Mais estável
- Valor médio (5): Recomendado
- Valor alto (10+): Mais rápido, mas pode sobrecarregar

### Pasta de Salvamento
- **Windows**: `C:\Users\SeuUsuario\Documents\cadernos`
- **Linux/Mac**: `/home/usuario/cadernos`
- A pasta será criada automaticamente se não existir

## 🔧 Solução de Problemas

### Erro 403 ao baixar
A API do PJe só funciona no Brasil. Execute de uma conexão brasileira.

### PyPDF2 não instalado
```bash
pip install PyPDF2
```

### Porta 5000 já em uso
Mude a porta no `app.py` ou encerre o processo que está usando:
```bash
# Linux/Mac
lsof -ti:5000 | xargs kill

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Busca não encontra nada
1. Certifique-se de que você já baixou documentos
2. Verifique se os documentos contêm o termo
3. Para PDFs, o PyPDF2 precisa estar instalado

### Aplicação lenta
1. Reduza o número de workers
2. Busque em menos tribunais por vez
3. Use filtros de data mais restritos

## 🌟 Dicas de Uso

### Workflow Recomendado
1. **Configure a pasta** no primeiro uso
2. **Baixe documentos** de interesse (por tribunal, data ou período)
3. **Busque termos** quantas vezes precisar
4. **Novos downloads** serão adicionados ao índice automaticamente

### Buscas Eficientes
- Use termos específicos para melhores resultados
- Busque por CPF/CNPJ sem pontuação
- Busque por números de processo
- Use palavras-chave do caso

### Organização
- Os arquivos são organizados automaticamente por:
  - Tribunal (sigla)
  - Ano
  - Mês
  - Nome: `SIGLA_DATA_TIPO.extensao`

### Automação
Execute a aplicação como serviço para acesso contínuo:
```bash
# Linux (systemd)
sudo nano /etc/systemd/system/pje-cadernos.service

# Adicione:
[Unit]
Description=Baixador PJe

[Service]
User=seu_usuario
WorkingDirectory=/caminho/para/cadernos
ExecStart=/usr/bin/python3 app.py

[Install]
WantedBy=multi-user.target

# Ative:
sudo systemctl enable pje-cadernos
sudo systemctl start pje-cadernos
```

## 📊 API REST

A aplicação também expõe uma API REST para integração:

### GET /api/config
Retorna configurações atuais

### POST /api/config
Atualiza configurações
```json
{
  "pasta_salvamento": "/caminho/pasta",
  "workers": 5
}
```

### GET /api/tribunais
Lista todos os tribunais disponíveis

### POST /api/baixar
Inicia download
```json
{
  "tribunais": ["TJSP", "TRF3"],
  "data_inicio": "01/11/2025",
  "data_fim": "05/11/2025",
  "tipos": ["E", "D"]
}
```

### GET /api/status
Retorna status do download em andamento

### POST /api/buscar
Busca termo nos documentos
```json
{
  "termo": "palavra"
}
```

### GET /api/estatisticas
Retorna estatísticas gerais

## 🎨 Personalização

### Trocar Cores
Edite `static/style.css`:
```css
/* Linha 5 - Gradiente principal */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Mude para suas cores favoritas */
background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
```

### Adicionar Logo
Edite `templates/index.html` e `templates/busca.html`:
```html
<header>
    <img src="/static/logo.png" alt="Logo" style="max-width: 200px;">
    <h1>📚 Baixador de Cadernos PJe</h1>
</header>
```

## 📝 Licença

MIT License - Use livremente!

## 🤝 Contribuindo

Contribuições são bem-vindas! Abra issues ou pull requests.

## ⚠️ Avisos Legais

- Acessa apenas dados públicos dos tribunais
- Respeite os limites da API
- Use de forma responsável
- Mantenha seus dados seguros
