# MUSSA v1.1

## CONFIGURACIÓN INICIAL

## Instalar Docker

Instalar Docker

    https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-convenience-script

    sudo apt-get install docker.io

Instalar Docker Compose

    https://docs.docker.com/compose/install/#install-compose

## Configuración SMTP

Editar la configuración del archivo app/local_settings.py

Especificar los datos de las configuraciones de variables MAIL_... para que coincidan con tus configuraciones de SMTP

Notar que el server SMTP de Google requiere la configuración de "less secure apps".
Ver: https://support.google.com/accounts/answer/6010255?hl=en

## Actualizar claves

Crear un archivo en el directorio MUSSA llamdo .env
Copiar el contenido de MUSSA/env_example. Actualizar los valores de las claves y distintas variables de entorno que se encuntran en MUSSA/.env

Copiar y actualizar las configuraciones locales:

    cp MUSSA/MUSSA_Flask/app/local_settings_example.py MUSSA/MUSSA_Flask/app/local_settings.py 

## Para ejecutar Docker (y la aplicación)

Acceder a la carpeta MUSSA en la que se ecnuentra el archivo docker y ejecutar el build:
(El build solo es necesario si se modificaron las dependencias)

    docker-compose up [--build]

## Si se desea parar los procesos de docker:

    docker-compose stop

## Para ver los procesos que se están ejecutando:

    docker-compose ps

## Ejecutar la aplicación

Apuntar el browser a http://localhost:5000/

Se pueden utilizar los siguientes usuarios:

    - email `member@example.com` - Contraseña: `Password1`.
    - email `admin@example.com` - Contraseña: `Password1`.

## Si se desea purgar las tareas pendientes de los workers

    celery -A AsyncTasks.AsyncTaskPLE.broker_generador_plan_ple purge
    celery -A app.API_Rest.GeneradorPlanCarreras.broker_guardar_plan_generado purge

## Autores

- Jennifer Andrea Woites

## Colaboradores (en el orden en el que se unieron al proyecto)

- Ariel Wainer

## Acknowledgements

With thanks to the following Flask extensions:

* [Alembic](http://alembic.zzzcomputing.com/)
* [Flask](http://flask.pocoo.org/)
* [Flask-Login](https://flask-login.readthedocs.io/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/)
* [Flask-Script](https://flask-script.readthedocs.io/)
* [Flask-User](http://flask-user.readthedocs.io/en/v0.6/)
* [Flask-User-starter-app](https://github.com/lingthio/Flask-User-starter-app) was used as a starting point for this code repository.