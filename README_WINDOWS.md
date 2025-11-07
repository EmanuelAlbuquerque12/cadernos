# 🪟 Guia Windows - Baixador de Cadernos PJe

Guia completo para usar no Windows com arquivos `.bat` de um clique!

## 🚀 Início Rápido (3 passos)

### 1️⃣ Primeira Vez - Instalar Dependências

**Duplo clique em:**
```
INSTALAR_DEPENDENCIAS.bat
```

Isso vai:
- ✅ Verificar se Python está instalado
- ✅ Instalar Flask, PyPDF2, Requests
- ✅ Preparar tudo automaticamente

**Tempo:** ~2-3 minutos

### 2️⃣ Criar Atalho na Área de Trabalho (Opcional)

**Duplo clique em:**
```
CRIAR_ATALHO.bat
```

Cria um atalho conveniente na sua área de trabalho!

### 3️⃣ Iniciar a Aplicação

**Duplo clique em:**
```
INICIAR.bat
```

Pronto! O navegador abre automaticamente! 🎉

---

## 📋 Arquivos .bat Disponíveis

### 🟢 INICIAR.bat (PRINCIPAL)
**Use este!** Arquivo principal para iniciar.

**O que faz:**
1. ✅ Verifica se Python está instalado
2. ✅ Verifica se dependências estão instaladas
3. ✅ Instala automaticamente se faltar algo
4. ✅ Inicia a aplicação
5. ✅ Abre o navegador automaticamente

**Como usar:**
- Duplo clique
- Aguarde a janela preta abrir
- Navegador abre sozinho
- **NÃO FECHE A JANELA PRETA!**

---

### 📦 INSTALAR_DEPENDENCIAS.bat
Instala todas as dependências necessárias.

**Quando usar:**
- Primeira vez que usar o programa
- Após atualizar o Python
- Se der erro de módulo não encontrado

**Como usar:**
- Duplo clique
- Aguarde a instalação (2-3 minutos)
- Veja "Instalação Concluída"
- Pronto para usar INICIAR.bat

---

### ⚡ INICIAR_RAPIDO.bat
Versão rápida sem verificações.

**Quando usar:**
- Se já instalou tudo antes
- Para iniciar mais rápido
- Pula verificações

**Mais rápido, mas não verifica problemas!**

---

### 🔗 CRIAR_ATALHO.bat
Cria atalho na área de trabalho.

**O que faz:**
- Cria atalho "Baixador Cadernos PJe"
- Coloca na sua área de trabalho
- Duplo clique no atalho = inicia programa

**Use uma vez, ganhe comodidade para sempre!**

---

### 🏗️ build.bat
Gera o executável .exe (avançado).

**Para desenvolvedores:**
- Gera arquivo .exe standalone
- Usuários não precisam de Python
- Distribuição facilitada

---

## ❓ Problemas Comuns

### "Python não encontrado"

**Problema:** Python não está instalado ou não está no PATH.

**Solução:**
1. Baixe Python: https://www.python.org/downloads/
2. **IMPORTANTE:** Marque "Add Python to PATH" na instalação
3. Reinicie o computador
4. Tente novamente

---

### "pip não é reconhecido"

**Problema:** pip não está no PATH.

**Solução:**
```batch
python -m pip install -r requirements.txt
```

Ou reinstale Python marcando "Add to PATH".

---

### Janela fecha muito rápido

**Problema:** Erro acontece mas janela fecha antes de ler.

**Solução:**
1. Abra CMD manualmente (Win + R, digite `cmd`)
2. Navegue até a pasta: `cd C:\caminho\para\cadernos`
3. Execute: `INICIAR.bat`
4. Agora consegue ler o erro

---

### "Acesso negado" ao instalar

**Problema:** Sem permissões de administrador.

**Solução:**
- Clique com botão direito no .bat
- "Executar como Administrador"
- Tente novamente

---

### Antivírus bloqueia

**Problema:** Antivírus detecta como suspeito.

**Solução:**
- Normal para arquivos .bat
- Adicione exceção no antivírus
- Ou desabilite temporariamente

---

### Porta 5000 em uso

**Problema:** Outro programa usando porta 5000.

**Solução:**
- O programa encontra automaticamente outra porta (5001-5009)
- Veja na mensagem qual porta foi usada
- Acesse: http://localhost:PORTA

---

## 🎯 Workflow Recomendado

### Primeira Vez:
```
1. INSTALAR_DEPENDENCIAS.bat  (uma vez)
2. CRIAR_ATALHO.bat            (opcional)
3. INICIAR.bat                 (sempre que usar)
```

### Próximas Vezes:
```
- Duplo clique no atalho da área de trabalho
  OU
- Duplo clique em INICIAR.bat
```

### Para Mais Velocidade:
```
- INICIAR_RAPIDO.bat (se já tem tudo instalado)
```

---

## 🔒 Segurança

### Os arquivos .bat são seguros?

✅ **SIM!** Você pode abrir em bloco de notas e ver o código.

**O que eles fazem:**
- Verificam se Python existe
- Instalam bibliotecas públicas (Flask, Requests)
- Iniciam a aplicação Python
- **NÃO** fazem nada malicioso

### Como verificar?

Clique com botão direito > "Editar" para ver o código.

---

## 💡 Dicas

### Dica 1: Mantenha a janela preta aberta
A janela preta (CMD) é o servidor. Fechar = aplicação para.

### Dica 2: Use o atalho
Crie com CRIAR_ATALHO.bat para facilitar sua vida!

### Dica 3: Configure a pasta
Na primeira vez, configure onde quer salvar os cadernos.

### Dica 4: Antivírus
Adicione exceção para a pasta do projeto para evitar problemas.

### Dica 5: Atualizações
Se atualizar o código, execute INSTALAR_DEPENDENCIAS.bat novamente.

---

## 🎨 Personalização

### Mudar título da janela

Edite o .bat:
```batch
title Seu Titulo Aqui
```

### Mudar cores

Adicione no início do .bat:
```batch
color 0A    :: Verde no preto
color 1F    :: Branco no azul
color 4E    :: Amarelo no vermelho
```

### Adicionar logo/texto

Adicione `echo` com ASCII art:
```batch
echo  ____  _____
echo |  _ \|  ___|
echo | |_) | |_
echo |  __/|  _|
echo |_|   |_|
```

---

## 🚀 Para Usuários Avançados

### Executar em porta específica

Edite `app.py`:
```python
porta = 8080  # Sua porta
```

### Modo debug

Edite INICIAR.bat, adicione:
```batch
set FLASK_DEBUG=1
python app.py
```

### Log em arquivo

Redirecione saída:
```batch
python app.py > log.txt 2>&1
```

### Iniciar minimizado

Use VBScript ou atalho configurado para iniciar minimizado.

---

## 📞 Suporte

### Erros Comuns:
1. Leia a mensagem de erro
2. Veja seção "Problemas Comuns" acima
3. Execute manualmente no CMD para ver erro completo

### Reportar Problema:
1. Anote a mensagem de erro completa
2. Anote sua versão do Python (`python --version`)
3. Abra issue no GitHub com detalhes

---

## 🎉 Pronto!

Com os arquivos .bat, usar o Baixador de Cadernos é:

1. **INSTALAR_DEPENDENCIAS.bat** (primeira vez)
2. **INICIAR.bat** (sempre que usar)
3. **Profit!** 🚀

**Simples assim!**

Duplo clique e navegador abre automaticamente.

Não precisa saber Python, não precisa saber linha de comando.

**Just works!** ✨

---

## 📚 Mais Informações

- **README.md** - Visão geral completa
- **README_WEB.md** - Guia da aplicação web
- **COMO_GERAR_EXE.md** - Criar executável .exe
- **INICIO_RAPIDO.md** - Guia rápido geral

---

**Desenvolvido com ❤️ para facilitar sua vida!**

Qualquer dúvida, consulte a documentação ou abra uma issue.
