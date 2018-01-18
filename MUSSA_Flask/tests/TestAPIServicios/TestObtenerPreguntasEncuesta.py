if __name__ == '__main__':
    import sys

    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase
from app.DAO.EncuestasDAO import *
from app.API_Rest.services import *
from app.API_Rest.codes import *
import json


class TestObtenerPreguntasEncuesta(TestBase):
    ##########################################################
    ##                   Configuracion                      ##
    ##########################################################

    def get_test_name(self):
        return "test_obtener_padron_alumno"

    def crear_datos_bd(self):
        create_encuestas()

    ##########################################################
    ##                      Tests                           ##
    ##########################################################

    def test_obtener_todas_las_preguntas_sin_filtrar_las_obtiene_a_todas(self):
        client = self.app.test_client()
        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE)
        assert (response.status_code == SUCCESS_OK)

        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        assert (len(preguntas) == 32)

    def test_obtener_todas_las_preguntas_de_una_categoria_solo_devuelve_las_de_dicha_categoria(self):
        parametros = {"categorias": GRUPO_ENCUESTA_DOCENTES}

        client = self.app.test_client()
        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        assert (len(preguntas) == 1)

    def test_obtener_todas_las_preguntas_de_varias_categorias_solo_devuelve_las_de_dichas_categorias(self):
        parametros = {"categorias": str(GRUPO_ENCUESTA_CLASES) + ";" + str(GRUPO_ENCUESTA_DOCENTES)}

        client = self.app.test_client()
        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        assert (len(preguntas) == 6)

    def test_obtener_todas_las_preguntas_de_categoria_inexistente_da_error(self):
        parametros = {"categorias": 89}

        client = self.app.test_client()
        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_obtener_todas_las_preguntas_de_categoria_invalida_da_error(self):
        parametros = {"categorias": "da9"}

        client = self.app.test_client()
        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_obtener_todas_las_preguntas_de_varias_categorias_existentes_mal_separador_da_error(self):
        parametros = {"categorias": str(GRUPO_ENCUESTA_CLASES) + "-" + str(GRUPO_ENCUESTA_DOCENTES)}

        client = self.app.test_client()
        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)


if __name__ == '__main__':
    import unittest

    unittest.main()
