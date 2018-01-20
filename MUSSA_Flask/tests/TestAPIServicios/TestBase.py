import app
import os
from flask_testing import TestCase
from flask import url_for
from app import db
from app.ClienteAPI.ClienteAPI import ClienteAPI

from app.DAO.UsersDAO import create_users
from app.DAO.MateriasDAO import create_estados_materia, create_forma_aprobacion_materias

from app.models.user_models import User


class TestBase(TestCase):
    ADMIN_MAIL = 'admin@example.com'
    MEMBER_MAIL = 'member@example.com'
    PASSWORD = "Password1"

    def get_test_db_name(self):
        return "sqlite:///tmp/" + self.get_test_name() + ".sql"

    def get_test_name(self):
        return "test_base"

    def create_app(self):
        settings = {}
        settings['SQLALCHEMY_DATABASE_URI'] = self.get_test_db_name()
        settings['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        settings['WTF_CSRF_METHODS'] = []
        settings['TESTING'] = True
        settings['WTF_CSRF_ENABLED'] = False
        settings['DEBUG'] = True

        extension_path = []
        path_actual = os.getcwd()
        while (not (len(extension_path) > 0 and extension_path[0] == 'tests')):
            path_separado = os.path.split(path_actual)
            extension_path.insert(0, path_separado[-1])
            path_actual = path_separado[0]

        pasos_retroceder = [".." for directorio in extension_path]
        os.chdir(os.path.join(*pasos_retroceder))

        self.app = app.create_app(extra_config_settings=settings)

        os.chdir(os.path.join('.', *extension_path))
        return self.app

    def do_login(self, data):
        client = self.app.test_client()
        client.post(url_for('user.login'), data=data)
        return client

    def loguear_usuario(self):
        return self.do_login({"email": self.MEMBER_MAIL, "password": self.PASSWORD})

    def loguear_administrador(self):
        return self.do_login({"email": self.ADMIN_MAIL, "password": self.PASSWORD})

    def get_usuario(self):
        return User.query.filter_by(email=self.MEMBER_MAIL).first()

    def get_administrador(self):
        return User.query.filter_by(email=self.ADMIN_MAIL).first()

    def setUp(self):
        db.create_all()
        create_users()
        create_estados_materia()
        create_forma_aprobacion_materias()
        db.session.commit()

        self.crear_datos_bd()
        db.session.commit()

    def crear_datos_bd(self):
        raise Exception("Debe implementarse en las clases hijas")

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def get_url_get_docente(self, idDocente):
        return ClienteAPI().get_url_get_docente(idDocente)

    def get_url_obtener_todos_los_docentes(self):
        return ClienteAPI().get_url_obtener_todos_los_docentes()

    def get_url_obtener_todas_las_carreras(self):
        return ClienteAPI().get_url_get_carreras()

    def get_url_get_materia(self, idMateria):
        return ClienteAPI().get_url_get_materia(idMateria)

    def get_url_get_materias(self):
        return ClienteAPI().get_url_get_materias()

    def get_url_materias_correlativas(self, idMateria):
        return ClienteAPI().get_url_materias_correlativas(idMateria)

    def get_url_get_curso(self, idCurso):
        return ClienteAPI().get_url_get_curso(idCurso)

    def get_url_all_cursos(self):
        return ClienteAPI().get_url_all_cursos()

    def get_url_obtener_todas_las_tematicas(self):
        return ClienteAPI().get_url_obtener_todas_las_tematicas()

    def get_url_preguntas_encuesta(self):
        return ClienteAPI().get_url_preguntas_encuesta()

    def get_url_get_alumno(self):
        return ClienteAPI().get_url_get_alumno()
