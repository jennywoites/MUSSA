from flask import Flask
from flask_testing import LiveServerTestCase
import unittest
import requests
import app

from flask_testing import TestCase
from app import create_app, db


class TestBase(TestCase):
    def get_test_db_name(self):
        return "sqlite:///tmp/" + self.get_test_name() + ".sql"

    def get_test_name(self):
        return "test_base"

    def create_app(self):
        settings = {}
        settings['SQLALCHEMY_DATABASE_URI'] = self.get_test_db_name()
        self.app = app.create_app(extra_config_settings=settings)
        return self.app

    def setUp(self):
        db.create_all()
        self.crear_datos_bd()
        db.session.commit()

    def crear_datos_bd(self):
        raise Exception("Debe implementarse en las clases hijas")

    def tearDown(self):
        db.session.remove()
        db.drop_all()
