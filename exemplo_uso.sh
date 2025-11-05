#!/bin/bash
# Exemplos de uso do baixador de cadernos do PJe

echo "================================"
echo "Exemplos de Uso - Baixador PJe"
echo "================================"
echo ""

# 1. Baixar cadernos de hoje de tribunais específicos
echo "1. Baixando cadernos de hoje do STJ e STF..."
python baixador_cadernos.py --tribunal STJ STF
echo ""

# 2. Baixar apenas editais de uma data específica
echo "2. Baixando apenas Editais de 05/11/2025 do TJSP..."
python baixador_cadernos.py --data 05/11/2025 --tipo E --tribunal TJSP
echo ""

# 3. Baixar período específico
echo "3. Baixando cadernos de 01/11/2025 a 05/11/2025 do TRF3..."
python baixador_cadernos.py --data-inicio 01/11/2025 --data-fim 05/11/2025 --tribunal TRF3
echo ""

# 4. Baixar de todos os TRFs
echo "4. Baixando de todos os Tribunais Regionais Federais..."
python baixador_cadernos.py --tribunal TRF1 TRF2 TRF3 TRF4 TRF5 TRF6
echo ""

# 5. Baixar com mais workers (mais rápido)
echo "5. Baixando com 10 workers paralelos..."
python baixador_cadernos.py --tribunal TJSP TJRJ --workers 10
echo ""

echo "================================"
echo "Exemplos concluídos!"
echo "Verifique o diretório 'cadernos_baixados' para ver os arquivos"
echo "================================"
