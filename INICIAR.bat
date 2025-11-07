@echo off
REM ========================================
REM  Baixador de Cadernos PJe - INICIO
REM ========================================
REM Duplo clique para iniciar!

title Baixador de Cadernos PJe

echo.
echo ========================================
echo   Baixador de Cadernos PJe
echo ========================================
echo.

REM Verifica se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale o Python 3.6 ou superior:
    echo https://www.python.org/downloads/
    echo.
    echo Marque a opcao "Add Python to PATH" durante a instalacao!
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado!
python --version
echo.

REM Verifica se as dependencias estao instaladas
echo Verificando dependencias...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo.
    echo [AVISO] Dependencias nao instaladas!
    echo Instalando automaticamente...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [ERRO] Falha ao instalar dependencias!
        echo Tente executar manualmente: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [OK] Dependencias instaladas com sucesso!
) else (
    echo [OK] Dependencias OK!
)

echo.
echo ========================================
echo   INICIANDO APLICACAO...
echo ========================================
echo.
echo O navegador abrira automaticamente.
echo.
echo IMPORTANTE:
echo - NAO FECHE ESTA JANELA!
echo - Use o navegador para interagir
echo - Pressione Ctrl+C aqui para encerrar
echo.
echo ========================================
echo.

REM Inicia a aplicacao
python app.py

REM Se o usuario fechar o Python
echo.
echo ========================================
echo   Aplicacao Encerrada
echo ========================================
echo.
pause
