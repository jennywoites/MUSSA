if __name__ == '__main__':
    import sys

    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase
from tests.TestAPIServicios.DAOMock.CarreraDAOMock import CarreraDAOMock, LICENCIATURA_EN_SISTEMAS_1986, \
    INGENIERIA_EN_INFORMATICA_1986
import json
from app.API_Rest.codes import *


class TestBuscarCarreras(TestBase):
    ##########################################################
    ##                   Configuracion                      ##
    ##########################################################

    def get_test_name(self):
        return "test_buscar_carreras"

    def crear_datos_bd(self):
        carreraDAOMock = CarreraDAOMock()
        carreraDAOMock.crear_licenciatura_en_sistemas_1986()
        carreraDAOMock.crear_ingenieria_informatica_1986()

    ##########################################################
    ##                Funciones Auxiliares                  ##
    ##########################################################

    def obtener_carreras(self, carreras):
        licenciatura = None
        ingenieria = None

        for carrera in carreras:
            if carrera["codigo"] == LICENCIATURA_EN_SISTEMAS_1986["codigo"]:
                licenciatura = carrera
            if carrera["codigo"] == INGENIERIA_EN_INFORMATICA_1986["codigo"]:
                ingenieria = carrera

        return ingenieria, licenciatura

    ##########################################################
    ##                      Tests                           ##
    ##########################################################

    def test_buscar_carreras_sin_parametros_devuelve_todas_las_carreras(self):
        client = self.app.test_client()
        response = client.get(self.get_url_obtener_todas_las_carreras())
        assert (response.status_code == SUCCESS_OK)

        carreras = json.loads(response.get_data(as_text=True))["carreras"]

        assert (len(carreras) == 2)

        ingenieria, licenciatura = self.obtener_carreras(carreras)

        assert (licenciatura is not None)
        assert (licenciatura["codigo"] == LICENCIATURA_EN_SISTEMAS_1986["codigo"])
        assert (licenciatura["nombre"] == LICENCIATURA_EN_SISTEMAS_1986["nombre"])

        assert (ingenieria is not None)
        assert (ingenieria["codigo"] == INGENIERIA_EN_INFORMATICA_1986["codigo"])
        assert (ingenieria["nombre"] == INGENIERIA_EN_INFORMATICA_1986["nombre"])


if __name__ == '__main__':
    import unittest

    unittest.main()
