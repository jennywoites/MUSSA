echo "Generando codigo PuLP..."
python3 007_generador_codigo_pulp_con_horarios.py

echo "Ejecutando codigo PuLP. Esto puede tardar algunos minutos..."
python3 pulp_001.py > resultado.txt

geany resultado.txt
