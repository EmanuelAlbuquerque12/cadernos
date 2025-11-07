@echo off
REM ========================================
REM  Criar Atalho na Area de Trabalho
REM  Baixador de Cadernos PJe
REM ========================================

title Criar Atalho - Baixador de Cadernos PJe

echo.
echo ========================================
echo   Criar Atalho na Area de Trabalho
echo ========================================
echo.

REM Obtém o diretório atual
set "SCRIPT_DIR=%~dp0"
set "DESKTOP=%USERPROFILE%\Desktop"

REM Cria o atalho usando PowerShell
echo Criando atalho...

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESKTOP%\Baixador Cadernos PJe.lnk'); $s.TargetPath = '%SCRIPT_DIR%INICIAR.bat'; $s.WorkingDirectory = '%SCRIPT_DIR%'; $s.Description = 'Baixador de Cadernos do PJe'; $s.Save()"

if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao criar atalho!
    echo Tente executar como Administrador.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   [SUCESSO] Atalho Criado!
echo ========================================
echo.
echo Um atalho foi criado na sua Area de Trabalho:
echo "Baixador Cadernos PJe"
echo.
echo Duplo clique nele para iniciar o programa!
echo.
pause
