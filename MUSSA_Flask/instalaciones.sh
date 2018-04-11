#Se genera el archivo de configuracion en base al de ejemplo
cp app/local_settings_example.py app/local_settings.py

sudo apt install coinor-cbc build-essential libmysqlclient-dev python-dev python3-dev libmysqlclient-dev mysql-server-5.7 redis-server libglpk-dev
sudo apt-get install python3-venv

# Crear la carpeta para el entorno virtual
mkdir venv
#Crear el entorno virtual
python3 -m venv venv
source venv/bin/activate

#Instalar dependencias
pip3 install -r requirements.txt
