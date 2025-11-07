@echo off
REM ========================================
REM  INICIO RAPIDO (sem verificacoes)
REM  Use se ja tiver tudo instalado
REM ========================================

title Baixador de Cadernos PJe - Inicio Rapido

cls
echo.
echo ========================================
echo   Baixador de Cadernos PJe
echo ========================================
echo.
echo Iniciando...
echo O navegador abrira automaticamente.
echo.
echo NAO FECHE ESTA JANELA!
echo.
echo ========================================
echo.

python app.py

echo.
echo Aplicacao encerrada.
timeout /t 3
