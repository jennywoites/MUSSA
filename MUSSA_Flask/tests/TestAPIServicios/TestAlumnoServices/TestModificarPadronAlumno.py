if __name__ == '__main__':
    import sys

    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase
from app.models.alumno_models import Alumno
from app.DAO.MateriasDAO import *
from app.API_Rest.services import *
from app.API_Rest.codes import *
import json


class TestModificarPadronAlumno(TestBase):
    ##########################################################
    ##                   Configuracion                      ##
    ##########################################################

    def get_test_name(self):
        return "test_modificar_padron_alumno"

    def crear_datos_bd(self):
        pass  # Los datos extras se crean dependiendo del test

    ##########################################################
    ##                      Tests                           ##
    ##########################################################

    def test_modificar_padron_sin_estar_logueado_da_error(self):
        client = self.app.test_client()
        response = client.post(self.get_url_get_alumno())
        assert (response.status_code == REDIRECTION_FOUND)

    def test_modificar_padron_logueado_con_administrador_esta_permitido(self):
        client = self.loguear_administrador()
        parametros = {"padron": "93274"}
        response = client.post(self.get_url_get_alumno(), data=parametros)
        assert (response.status_code == SUCCESS_OK)

    def test_modificar_padron_alumno_no_creado_deja_el_alumno_creado_con_el_padron_elegido(self):
        PADRON = "93724"
        client = self.loguear_usuario()
        parametros = {"padron": PADRON}
        response = client.post(self.get_url_get_alumno(), data=parametros)
        assert (response.status_code == SUCCESS_OK)

        alumno = Alumno.query.filter_by(user_id=self.get_usuario().id).first()
        assert (alumno.padron == PADRON)

    def test_modificar_padron_alumno_creado_sin_padron_guarda_el_alumno_con_el_padron_elegido(self):
        db.session.add(Alumno(user_id=self.get_usuario().id))
        db.session.commit()

        PADRON = "93724"
        client = self.loguear_usuario()
        parametros = {"padron": PADRON}
        response = client.post(self.get_url_get_alumno(), data=parametros)
        assert (response.status_code == SUCCESS_OK)

        alumno = Alumno.query.filter_by(user_id=self.get_usuario().id).first()
        assert (alumno.padron == PADRON)

    def test_modificar_padron_alumno_creado_con_padron_guarda_el_alumno_con_el_padron_elegido(self):
        db.session.add(Alumno(user_id=self.get_usuario().id, padron="88888"))
        db.session.commit()

        PADRON = "93724"
        client = self.loguear_usuario()
        parametros = {"padron": PADRON}
        response = client.post(self.get_url_get_alumno(), data=parametros)
        assert (response.status_code == SUCCESS_OK)

        alumno = Alumno.query.filter_by(user_id=self.get_usuario().id).first()
        assert (alumno.padron == PADRON)

    def test_modificar_padron_con_padron_utilizado_por_otro_alumno_da_error(self):
        db.session.add(Alumno(user_id=self.get_administrador().id, padron="88888"))
        db.session.commit()

        PADRON = "88888"
        client = self.loguear_usuario()
        parametros = {"padron": PADRON}
        response = client.post(self.get_url_get_alumno(), data=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_modificar_padron_con_padron_vacio_da_error(self):
        client = self.loguear_usuario()
        parametros = {"padron": ""}
        response = client.post(self.get_url_get_alumno(), data=parametros)
        assert (response.status_code == CLIENT_ERROR_NOT_FOUND)

    def test_modificar_padron_con_padron_numerico_longitud_menor_a_la_minima_de_cinco_da_error(self):
        client = self.loguear_usuario()
        parametros = {"padron": "1234"}
        response = client.post(self.get_url_get_alumno(), data=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_modificar_padron_con_padron_numerico_longitud_mayor_a_la_maxima_de_siete_da_error(self):
        client = self.loguear_usuario()
        parametros = {"padron": "12345678"}
        response = client.post(self.get_url_get_alumno(), data=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_modificar_padron_con_padron_no_numerico_da_error(self):
        client = self.loguear_usuario()
        parametros = {"padron": "125s7"}
        response = client.post(self.get_url_get_alumno(), data=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_modificar_padron_sin_parametros_da_error(self):
        client = self.loguear_usuario()
        response = client.post(self.get_url_get_alumno())
        assert (response.status_code == CLIENT_ERROR_NOT_FOUND)


if __name__ == '__main__':
    import unittest

    unittest.main()
