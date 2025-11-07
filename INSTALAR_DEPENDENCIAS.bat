@echo off
REM ========================================
REM  Instalador de Dependencias
REM  Baixador de Cadernos PJe
REM ========================================

title Instalando Dependencias - Baixador de Cadernos PJe

echo.
echo ========================================
echo   Instalador de Dependencias
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

REM Atualiza o pip
echo Atualizando pip...
python -m pip install --upgrade pip
echo.

REM Instala dependencias
echo ========================================
echo   Instalando Dependencias...
echo ========================================
echo.
echo Isso pode levar alguns minutos...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ========================================
    echo   [ERRO] Falha na instalacao!
    echo ========================================
    echo.
    echo Possiveis solucoes:
    echo 1. Verifique sua conexao com a internet
    echo 2. Execute como Administrador
    echo 3. Tente: python -m pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   [SUCESSO] Instalacao Concluida!
echo ========================================
echo.
echo Dependencias instaladas:
pip list | findstr /I "flask requests PyPDF2 urllib3"
echo.
echo Agora voce pode executar: INICIAR.bat
echo.
pause
