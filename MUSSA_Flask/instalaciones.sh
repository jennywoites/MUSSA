#Se genera el archivo de configuracion en base al de ejemplo
cp app/local_settings_example.py app/local_settings.py

sudo apt install build-essential python3-venv libmysqlclient-dev python-dev python3-dev libmysqlclient-dev mysql-server-5.7 redis-server libglpk-dev

# Crear la carpeta para el entorno virtual
mkdir venv
#Crear el entorno virtual
python3 -m venv venv
source venv/bin/activate

#Instalar dependencias
pip3 install -r requirements.txt