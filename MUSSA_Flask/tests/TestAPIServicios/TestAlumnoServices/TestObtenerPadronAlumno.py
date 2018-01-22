if __name__ == '__main__':
    import sys

    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase
from app.models.alumno_models import Alumno
from app.DAO.MateriasDAO import *
from app.API_Rest.services import *
from app.API_Rest.codes import *
import json


class TestObtenerPadronAlumno(TestBase):
    ##########################################################
    ##                   Configuracion                      ##
    ##########################################################

    def get_test_name(self):
        return "test_obtener_padron_alumno"

    def crear_datos_bd(self):
        pass  # Los datos extras se crean dependiendo del test

    ##########################################################
    ##                      Tests                           ##
    ##########################################################

    def test_obtener_padron_sin_estar_logueado_da_error(self):
        client = self.app.test_client()
        response = client.get(self.get_url_get_alumno())
        assert (response.status_code == REDIRECTION_FOUND)

    def test_obtener_padron_logueado_con_administrador_esta_permitido(self):
        client = self.loguear_administrador()
        response = client.get(self.get_url_get_alumno())
        assert (response.status_code == SUCCESS_OK)

    def test_obtener_padron_alumno_no_creado_de_usuario_valido(self):
        client = self.loguear_usuario()

        response = client.get(self.get_url_get_alumno())
        assert (response.status_code == SUCCESS_OK)

        padron = json.loads(response.get_data(as_text=True))["alumno"]["padron"]
        assert (padron == "")

    def test_obtener_padron_alumno_con_padron_vacio(self):
        alumno = Alumno(user_id=self.get_usuario().id, padron="")
        db.session.add(alumno)
        db.session.commit()

        client = self.loguear_usuario()
        response = client.get(self.get_url_get_alumno())
        assert (response.status_code == SUCCESS_OK)

        padron = json.loads(response.get_data(as_text=True))["alumno"]["padron"]
        assert (padron == "")

    def test_obtener_padron_alumno_con_padron_numerico(self):
        PADRON = "93274"
        alumno = Alumno(user_id=self.get_usuario().id, padron=PADRON)
        db.session.add(alumno)
        db.session.commit()

        client = self.loguear_usuario()
        response = client.get(self.get_url_get_alumno())
        assert (response.status_code == SUCCESS_OK)

        padron = json.loads(response.get_data(as_text=True))["alumno"]["padron"]
        assert (padron == PADRON)


if __name__ == '__main__':
    import unittest

    unittest.main()
