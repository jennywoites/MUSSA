echo "Generando codigo PuLP..."
python3 main.py

echo "Ejecutando codigo PuLP. Esto puede tardar algunos minutos..."
python3 pulp_001.py > resultado.txt

geany resultado.txt
