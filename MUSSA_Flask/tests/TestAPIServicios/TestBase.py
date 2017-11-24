from flask import Flask
from flask_testing import LiveServerTestCase
import unittest
import requests
import app

from flask_testing import TestCase, LiveServerTestCase
from flask import url_for
from flask_wtf.csrf import generate_csrf
from app import create_app, db

from app.DAO.UsersDAO import create_users
from app.DAO.MateriasDAO import create_estados_materia, create_forma_aprobacion_materias

from app.models.user_models import User


class TestBase(LiveServerTestCase):
    ADMIN_MAIL = 'admin@example.com'
    MEMBER_MAIL = 'member@example.com'
    PASSSWORD = "Password1"

    def get_test_db_name(self):
        return "sqlite:///tmp/" + self.get_test_name() + ".sql"


    def get_test_name(self):
        return "test_base"


    def create_app(self):
        settings = {}
        settings['SQLALCHEMY_DATABASE_URI'] = self.get_test_db_name()
        settings['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        # settings['WTF_CSRF_METHODS'] = []
        # self.test_port = 8080
        # settings['LIVESERVER_PORT'] = self.test_port
        self.app = app.create_app(extra_config_settings=settings)
        return self.app


    def loguear_usuario(self):
        client = self.app.test_client()
        data = {"email":self.MEMBER_MAIL, "password": self.PASSSWORD}
        url = 'http://localhost:%s%s' % (self.test_port, url_for('user.login')) 
        response = requests.post(url, data=data)    
        return response.cookies


    def loguear_administrador(self):
        client = self.app.test_client()
        data = {"email":self.ADMIN_MAIL, "password": self.PASSSWORD}
        url = 'http://localhost:%s%s' % (self.test_port, url_for('user.login')) 
        response = requests.post(url, data=data)    
        return response.cookies
        

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
