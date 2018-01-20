if __name__ == '__main__':
    import sys

    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase
from app import db
from app.models.carreras_models import Carrera
import json


class TestBuscarCarreras(TestBase):
    ##########################################################
    ##                   Configuracion                      ##
    ##########################################################

    def get_test_name(self):
        return "test_buscar_carreras"

    def crear_datos_bd(self):
        db.session.add(Carrera(
            codigo='9',
            nombre='Licenciatura en Análisis de Sistemas',
            duracion_estimada_en_cuatrimestres=9,
            requiere_prueba_suficiencia_de_idioma=False
        ))

        db.session.add(Carrera(
            codigo='10',
            nombre='Ingeniería en Informática',
            duracion_estimada_en_cuatrimestres=12,
            requiere_prueba_suficiencia_de_idioma=False
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

    def test_buscar_carreras_sin_parametros_devuelve_todas_las_carreras(self):
        client = self.app.test_client()
        response = client.get(self.get_url_obtener_todas_las_carreras())
        assert (response.status_code == 200)

        carreras = json.loads(response.get_data(as_text=True))["carreras"]

        assert (len(carreras) == 2)

        ingenieria, licenciatura = self.obtener_carreras(carreras)

        assert (licenciatura is not None)
        assert (licenciatura["codigo"] == '9')
        assert (licenciatura["nombre"] == 'Licenciatura en Análisis de Sistemas')

        assert (ingenieria is not None)
        assert (ingenieria["codigo"] == '10')
        assert (ingenieria["nombre"] == 'Ingeniería en Informática')


if __name__ == '__main__':
    import unittest

    unittest.main()