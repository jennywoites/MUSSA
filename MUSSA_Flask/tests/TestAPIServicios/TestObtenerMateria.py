if __name__ == '__main__':
    import os
    import sys

    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase

import app
from app import db
from app.models.carreras_models import Carrera, Materia, TipoMateria

from app.API_Rest.services import *
from app.API_Rest.codes import *

import json


class TestObtenerMateria(TestBase):
    ##########################################################
    ##                   Configuracion                      ##
    ##########################################################

    def get_test_name(self):
        return "test_obtener_materia"

    def crear_datos_bd(self):
        carrera = Carrera(
            codigo='9',
            nombre='Licenciatura en Análisis de Sistemas',
            duracion_estimada_en_cuatrimestres=9,
            requiere_prueba_suficiencia_de_idioma=False
        )
        db.session.add(carrera)

        tipo_materia = TipoMateria(descripcion="Tipo Materia Test")
        db.session.add(tipo_materia)
        db.session.commit()

        db.session.add(Materia(
            codigo="7575",
            nombre="Materia test",
            objetivos="Ninguno",
            creditos_minimos_para_cursarla=10,
            creditos=24,
            tipo_materia_id=tipo_materia.id,
            carrera_id=carrera.id
        ))

    ##########################################################
    ##                      Tests                           ##
    ##########################################################

    def test_obtener_materia_con_id_valido_devuelve_la_materia(self):
        materia_bdd = Materia.query.first()
        tipo = TipoMateria.query.first()
        carrera = Carrera.query.first()

        client = self.app.test_client()
        response = client.get(OBTENER_MATERIA_SERVICE, query_string={"id_materia": "1"})
        assert (response.status_code == SUCCESS_OK)

        materia = json.loads(response.get_data(as_text=True))["materia"]

        assert (materia_bdd.id == materia["id"])
        assert (materia_bdd.codigo == materia["codigo"])
        assert (materia_bdd.nombre == materia["nombre"])
        assert (materia_bdd.creditos == materia["creditos"])
        assert (materia_bdd.creditos_minimos_para_cursarla == materia["creditos_minimos_para_cursarla"])
        assert (tipo.descripcion == materia["tipo"])
        assert (carrera.id == materia["carrera_id"])
        assert (carrera.nombre == materia["carrera"])

    def test_obtener_materia_con_id_numerico_inexistente_devuelve_error(self):
        client = self.app.test_client()
        response = client.get(OBTENER_MATERIA_SERVICE, query_string={"id_materia": "10"})
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_obtener_materia_con_id_invalido_devuelve_error(self):
        client = self.app.test_client()
        response = client.get(OBTENER_MATERIA_SERVICE, query_string={"id_materia": "4sd0"})
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_obtener_materia_sin_parametors_devuelve_error(self):
        client = self.app.test_client()
        response = client.get(OBTENER_MATERIA_SERVICE)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)


if __name__ == '__main__':
    import unittest

    unittest.main()
