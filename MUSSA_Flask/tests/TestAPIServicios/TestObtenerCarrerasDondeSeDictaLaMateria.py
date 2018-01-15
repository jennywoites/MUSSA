if __name__ == '__main__':
    import sys

    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase
from app import db
from app.models.carreras_models import Carrera, Materia, TipoMateria
import json
from app.API_Rest.codes import *


class TestObtenerCarrerasDondeSeDictaLaMateria(TestBase):
    ##########################################################
    ##                   Configuracion                      ##
    ##########################################################

    def get_test_name(self):
        return "test_obtener_carreras_donde_se_dicta_la_materia"

    def crear_datos_bd(self):
        carrera1 = Carrera(
            codigo='9',
            nombre='Licenciatura en Análisis de Sistemas',
            duracion_estimada_en_cuatrimestres=9,
            requiere_prueba_suficiencia_de_idioma=False
        )
        db.session.add(carrera1)
        db.session.commit()

        carrera2 = Carrera(
            codigo='10',
            nombre='Ingeniería en Informática',
            duracion_estimada_en_cuatrimestres=12,
            requiere_prueba_suficiencia_de_idioma=False
        )
        db.session.add(carrera2)

        tipo = TipoMateria(descripcion="Un tipo")
        db.session.add(tipo)
        db.session.commit()

        db.session.add(Materia(
            codigo="9000",
            nombre="Materia con carrera 1",
            creditos_minimos_para_cursarla=0,
            creditos=10,
            tipo_materia_id=tipo.id,
            carrera_id=carrera1.id
        ))

        db.session.add(Materia(
            codigo="9000",
            nombre="Materia con carrera 2",
            creditos_minimos_para_cursarla=0,
            creditos=10,
            tipo_materia_id=tipo.id,
            carrera_id=carrera2.id
        ))

        db.session.add(Materia(
            codigo="8686",
            nombre="Materia 2 con carrera 1",
            creditos_minimos_para_cursarla=0,
            creditos=10,
            tipo_materia_id=tipo.id,
            carrera_id=carrera1.id
        ))

    ##########################################################
    ##                Funciones Auxiliares                  ##
    ##########################################################

    def obtener_carreras(self, carreras):
        licenciatura = None
        ingenieria = None

        for carrera in carreras:
            if carrera["codigo"] == '9':
                licenciatura = carrera
            if carrera["codigo"] == '10':
                ingenieria = carrera

        return ingenieria, licenciatura

    ##########################################################
    ##                      Tests                           ##
    ##########################################################

    def test_obtener_carreras_codigo_materia_con_mas_de_una_carrera_devuelve_todas_las_carreras(self):
        params = {"codigo_materia": "9000"}
        client = self.app.test_client()
        response = client.get(self.get_url_obtener_todas_las_carreras(), query_string=params)
        assert (response.status_code == SUCCESS_OK)

        carreras = json.loads(response.get_data(as_text=True))["carreras"]

        assert (len(carreras) == 2)

        ingenieria, licenciatura = self.obtener_carreras(carreras)

        assert (licenciatura is not None)
        assert (licenciatura["id_carrera"] == 1)
        assert (licenciatura["codigo"] == '9')
        assert (licenciatura["nombre"] == 'Licenciatura en Análisis de Sistemas')

        assert (ingenieria is not None)
        assert (ingenieria["id_carrera"] == 2)
        assert (ingenieria["codigo"] == '10')
        assert (ingenieria["nombre"] == 'Ingeniería en Informática')

    def test_obtener_carreras_codigo_materia_con_unica_carrera_devuelve_una_sola_carrera(self):
        params = {"codigo_materia": "8686"}
        client = self.app.test_client()
        response = client.get(self.get_url_obtener_todas_las_carreras(), query_string=params)
        assert (response.status_code == SUCCESS_OK)

        carreras = json.loads(response.get_data(as_text=True))["carreras"]

        assert (len(carreras) == 1)

        carrera = carreras[0]

        assert (carrera is not None)
        assert (carrera["id_carrera"] == 1)
        assert (carrera["codigo"] == '9')
        assert (carrera["nombre"] == 'Licenciatura en Análisis de Sistemas')

    def test_obtener_carreras_con_codigo_inexistente_devuelve_bad_request(self):
        params = {"codigo_materia": "8998"}
        client = self.app.test_client()
        response = client.get(self.get_url_obtener_todas_las_carreras(), query_string=params)
        assert (response.status_code == CLIENT_ERROR_NOT_FOUND)

    def test_obtener_carreras_con_codigo_invalido_devuelve_bad_request(self):
        params = {"codigo_materia": "8ad8"}
        client = self.app.test_client()
        response = client.get(self.get_url_obtener_todas_las_carreras(), query_string=params)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)


if __name__ == '__main__':
    import unittest

    unittest.main()
