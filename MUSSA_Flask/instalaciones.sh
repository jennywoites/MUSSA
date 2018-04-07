sudo apt-get install build-essential python3-venv libmysqlclient-dev python-dev python3-dev libmysqlclient-dev install mysql-server-5.7

# Crear la carpeta para el entorno virtual
mkdir venv
#Crear el entorno virtual
python3 -m venv venv
source venv/bin/activate

#Instalar dependencias
pip3 install -r requirements.txt