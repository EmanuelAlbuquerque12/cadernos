#!/bin/bash
# Script para iniciar a aplicação web do Baixador de Cadernos PJe

echo "==========================================="
echo "  Baixador de Cadernos PJe - Web App"
echo "==========================================="
echo ""

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "   Por favor, instale o Python 3.6 ou superior"
    exit 1
fi

echo "✓ Python encontrado: $(python3 --version)"
echo ""

# Verifica dependências
echo "Verificando dependências..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask não instalado. Instalando dependências..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao instalar dependências!"
        exit 1
    fi
    echo "✓ Dependências instaladas"
else
    echo "✓ Dependências OK"
fi
echo ""

# Inicia aplicação
echo "==========================================="
echo "  Iniciando servidor web..."
echo "==========================================="
echo ""
echo "  Acesse no navegador:"
echo "  👉 http://localhost:5000"
echo ""
echo "  Pressione Ctrl+C para parar"
echo "==========================================="
echo ""

python3 app.py
