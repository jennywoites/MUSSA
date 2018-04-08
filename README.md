# MUSSA v1.0

## Configuración inicial

Moverse a la carpeta MUSSA_Flask

    cd MUSSA_Flask

Ejecutar el script de instalacion (requiere permiso de ejecucion)

    instalaciones.sh


Instalar / Configurar base de datos MySQL

    mysqladmin -uroot -p create mussa # Nos va a solicitar el password PASSWORD_DB
    mysql -uroot -p # Nos va a solicitar el password PASSWORD_DB
    mysql> use mussa;
    mysql> grant all on * to 'mussa'@'localhost' identified by PASSWORD_ADMIN; # Se crea la password para el admin
    Ctrl-D
    
Cambiar en app/local_settings.py la SQLALCHEMY_DATABASE_URI

    SQLALCHEMY_DATABASE_URI = "mysql://mussa:PASSWORD_ADMIN@localhost/mussa"


## Configuración SMTP

Editar la configuración del archivo app/local_settings.py

Especificar los datos de las configuraciones de variables MAIL_... para que coincidan con tus configuraciones de SMTP

Notar que el server SMTP de Google requiere la configuración de "less secure apps".
Ver: https://support.google.com/accounts/answer/6010255?hl=en


## Inicializar la base de datos

    python3 manage.py init_db

## Actualizar las traducciones (no se encuentra en uso)
    
    pybabel update -d translations -D flask_user -i translations/flask_user.pot
    pybabel compile -d translations -D flask_user -f

## Ejecutar la aplicación

Inicializar el Web Server

    python3 manage.py runserver

Apuntar el browser a http://localhost:5000/

Se pueden utilizar los siguientes usuarios:

    - email `member@example.com` - Contraseña: `Password1`.
    - email `admin@example.com` - Contraseña: `Password1`.

## Inicializar los workers (para permitir la generación del plan de carrera)

    celery -A AsyncTasks.AsyncTaskGreedy.broker_generador_greedy worker --loglevel=debug
    celery -A AsyncTasks.AsyncTaskPLE.broker_generador_plan_ple worker --loglevel=debug
    celery -A app.API_Rest.GeneradorPlanCarreras.broker_guardar_plan_generado worker --loglevel=debug

## Si se desea purgar las tareas pendientes de los workers

    celery -A AsyncTasks.AsyncTaskGreedy.broker_generador_greedy purge
    celery -A AsyncTasks.AsyncTaskPLE.broker_generador_plan_ple purge
    celery -A app.API_Rest.GeneradorPlanCarreras.broker_guardar_plan_generado purge

## Acknowledgements

With thanks to the following Flask extensions:

* [Alembic](http://alembic.zzzcomputing.com/)
* [Flask](http://flask.pocoo.org/)
* [Flask-Login](https://flask-login.readthedocs.io/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/)
* [Flask-Script](https://flask-script.readthedocs.io/)
* [Flask-User](http://flask-user.readthedocs.io/en/v0.6/)
* [Flask-User-starter-app](https://github.com/lingthio/Flask-User-starter-app) was used as a starting point for this code repository.


## Autores

- Jennifer Andrea Woites