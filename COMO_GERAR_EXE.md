# 📦 Como Gerar o Executável (.exe)

Este guia mostra como criar um arquivo `.exe` do Baixador de Cadernos PJe que pode ser distribuído para usuários que não têm Python instalado.

## ✅ Pré-requisitos

- **Sistema Operacional:** Windows (recomendado Windows 10/11)
- **Python:** 3.6 ou superior instalado
- **Conexão com internet:** Para baixar dependências

## 🚀 Método 1: Automático (Recomendado)

### No Windows:

1. **Abra o Prompt de Comando** na pasta do projeto
2. Execute o script de build:
   ```batch
   build.bat
   ```
   ou
   ```batch
   python build_exe.py
   ```

3. **Aguarde** o processo (pode levar alguns minutos)

4. **Pronto!** O executável estará em:
   ```
   dist/BaixadorCadernosPJe.exe
   ```

## 🔧 Método 2: Manual

Se preferir fazer manualmente:

### Passo 1: Instalar PyInstaller

```bash
pip install pyinstaller
```

### Passo 2: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 3: Gerar o Executável

```bash
pyinstaller --clean --noconfirm BaixadorCadernosPJe.spec
```

### Passo 4: Localizar o .exe

O arquivo será criado em:
```
dist/BaixadorCadernosPJe.exe
```

## 📋 O que o build faz?

1. ✅ Verifica se PyInstaller está instalado
2. ✅ Verifica todas as dependências
3. ✅ Remove builds antigos
4. ✅ Empacota Python + bibliotecas + código
5. ✅ Inclui templates HTML e CSS
6. ✅ Inclui arquivo de tribunais
7. ✅ Cria executável único de ~50-80 MB
8. ✅ Gera README para distribuição

## 📊 Tamanho do Executável

- **Tamanho típico:** 50-80 MB
- **Contém:** Python + Flask + todas as bibliotecas
- **Vantagem:** Usuário não precisa instalar nada!

## 🎯 Como Usar o .exe Gerado

### Para você (desenvolvedor):

1. Localize: `dist/BaixadorCadernosPJe.exe`
2. Teste executando o arquivo
3. Distribua para usuários

### Para o usuário final:

1. **Baixe** o arquivo `BaixadorCadernosPJe.exe`
2. **Duplo clique** no arquivo
3. **Aguarde** o navegador abrir automaticamente
4. **Pronto!** Comece a usar

**Importante para o usuário:**
- ⚠️ Não feche a janela preta (console) enquanto usar
- 📁 Configure a pasta de salvamento na primeira vez
- 🔍 A busca funciona nos documentos já baixados

## ⚠️ Problemas Comuns

### Antivírus bloqueia o .exe

**Normal!** Executáveis gerados com PyInstaller podem ser detectados como suspeitos.

**Soluções:**
1. Adicione exceção no antivírus
2. Execute como administrador
3. Use certificado digital (avançado)

### Erro "ModuleNotFoundError"

**Causa:** Faltou incluir algum módulo

**Solução:**
1. Abra `BaixadorCadernosPJe.spec`
2. Adicione o módulo em `hiddenimports`
3. Gere novamente: `pyinstaller BaixadorCadernosPJe.spec`

### .exe muito grande (>100 MB)

**Normal!** Inclui Python completo + bibliotecas.

**Para reduzir (opcional):**
```bash
pip install upx
# Recompile
```

### Erro ao executar o .exe

**Teste em outro PC Windows** - pode ser problema local

**Verifique:**
1. Windows atualizado
2. Microsoft Visual C++ Redistributable instalado
3. Firewall não está bloqueando

## 🔐 Segurança

### Para desenvolvedores:

- ✅ Código-fonte aberto e auditável
- ✅ Não coleta dados do usuário
- ✅ Roda localmente na máquina
- ✅ Sem conexões suspeitas

### Para usuários:

- ⚠️ Baixe apenas de fontes confiáveis
- ✓ Verifique assinatura digital (se disponível)
- ✓ Use antivírus atualizado
- ✓ O programa acessa apenas APIs públicas do PJe

## 📦 Distribuição

### Opção 1: Arquivo Único

Distribua apenas:
```
BaixadorCadernosPJe.exe
```

**Vantagens:**
- Simples
- Usuário só baixa um arquivo

**Desvantagens:**
- Grande (50-80 MB)

### Opção 2: Com Instalador

Crie instalador com:
- NSIS
- Inno Setup
- InstallForge

**Vantagens:**
- Profissional
- Pode criar atalhos
- Pode adicionar ícone na área de trabalho

### Opção 3: Portable ZIP

Compacte a pasta `dist/` inteira:

```
BaixadorCadernosPJe.zip
  ├── BaixadorCadernosPJe.exe
  └── LEIA-ME.txt
```

## 🎨 Personalização

### Adicionar Ícone

1. Crie ou baixe um arquivo `icon.ico`
2. Coloque na raiz do projeto
3. O build usará automaticamente

### Mudar Nome do .exe

Edite `BaixadorCadernosPJe.spec`:
```python
name='SeuNomeAqui',
```

### Versão sem Console

Para esconder a janela preta:

Edite `BaixadorCadernosPJe.spec`:
```python
console=False,  # Mude de True para False
```

**Atenção:** Usuário não verá mensagens de erro!

## 🐧 Linux / Mac

PyInstaller funciona em Linux/Mac também!

### Linux:
```bash
python build_exe.py
# Gera executável ELF
```

### Mac:
```bash
python build_exe.py
# Gera app bundle (.app)
```

**Nota:** Cada sistema gera executável para si mesmo. Para gerar .exe para Windows, **deve** estar no Windows.

## 📚 Recursos

- [PyInstaller Docs](https://pyinstaller.org/)
- [PyInstaller no GitHub](https://github.com/pyinstaller/pyinstaller)
- [Como Assinar .exe](https://docs.microsoft.com/en-us/windows/win32/seccrypto/cryptography-tools)

## 💡 Dicas

### Teste Antes de Distribuir

1. Teste em máquina limpa (sem Python)
2. Teste com antivírus ativo
3. Teste em Windows 10 e 11
4. Peça feedback de usuários beta

### Versioning

Adicione número de versão:
```python
name='BaixadorCadernosPJe-v1.0',
```

### Comprimir com UPX

Para executáveis menores:
```bash
pip install upx
# Rebuild
```

## ❓ FAQ

**P: Preciso comprar licença do PyInstaller?**
R: Não! PyInstaller é open-source e gratuito.

**P: Posso vender o .exe?**
R: Depende da licença do seu projeto. Este projeto é MIT.

**P: O .exe funciona offline?**
R: Sim! Mas precisa internet para baixar cadernos do PJe.

**P: Quanto tempo leva para gerar?**
R: 2-5 minutos dependendo do PC.

**P: Posso automatizar builds?**
R: Sim! Use CI/CD (GitHub Actions, etc.)

## 🆘 Suporte

Se tiver problemas:

1. Leia as mensagens de erro
2. Verifique issues no GitHub
3. Consulte docs do PyInstaller
4. Abra uma issue detalhada

---

**Pronto para distribuir!** 🚀

Seu executável está em `dist/BaixadorCadernosPJe.exe`

Os usuários vão adorar não precisar instalar Python! 😄
