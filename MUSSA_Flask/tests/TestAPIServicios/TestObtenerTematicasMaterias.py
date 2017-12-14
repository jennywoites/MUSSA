if __name__ == '__main__':
    import sys

    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase
from app.models.palabras_clave_models import TematicaMateria
from app.DAO.MateriasDAO import *
from app.API_Rest.services import *
from app.API_Rest.codes import *
import json


class TestObtenerTematicasMaterias(TestBase):

    TEMA_1 = {
        "id": 1,
        "tema": "TEMA1"
    }

    TEMA_2 = {
        "id": 2,
        "tema": "TEMA2"
    }

    TEMA_3 = {
        "id": 3,
        "tema": "TEMA3"
    }

    ##########################################################
    ##                   Configuracion                      ##
    ##########################################################

    def get_test_name(self):
        return "test_obtener_tematicas_materia"

    def crear_datos_bd(self):
        pass  # Los datos extras se crean dependiendo del test

    def crear_tematica(self, dic_tematica):
        db.session.add(TematicaMateria(
            tematica=dic_tematica["tema"]
        ))
        db.session.commit()

    ##########################################################
    ##              Funciones Auxiliares                    ##
    ##########################################################

    def se_encuentra_la_tematica(self, tematica_origen, l_tematicas):
        for tematica_servidor in l_tematicas:
            if self.tematicas_son_iguales(tematica_origen, tematica_servidor):
                return True
        return False

    def tematicas_son_iguales(self, origen, servidor):
        return (origen["id"] == servidor["id"] and
                origen["tema"] == servidor["tema"] )

    ##########################################################
    ##                      Tests                           ##
    ##########################################################

    def test_obtener_tematicas_sin_existir_en_la_base_de_datos_devuelve_lista_vacia(self):
        client = self.loguear_usuario()

        response = client.get(OBTENER_TEMATICAS_MATERIAS)
        assert (response.status_code == SUCCESS_OK)

        tematicas = json.loads(response.get_data(as_text=True))["tematicas"]
        assert (len(tematicas) == 0)

    def test_obtener_tematicas_con_datos_en_la_base_de_datos_devuelve_todas_las_tematicas(self):
        self.crear_tematica(self.TEMA_1)
        self.crear_tematica(self.TEMA_2)
        self.crear_tematica(self.TEMA_3)

        client = self.loguear_usuario()

        response = client.get(OBTENER_TEMATICAS_MATERIAS)
        assert (response.status_code == SUCCESS_OK)

        tematicas = json.loads(response.get_data(as_text=True))["tematicas"]
        assert (len(tematicas) == 3)

        self.se_encuentra_la_tematica(self.TEMA_1, tematicas)
        self.se_encuentra_la_tematica(self.TEMA_2, tematicas)
        self.se_encuentra_la_tematica(self.TEMA_3, tematicas)

    def test_obtener_tematicas_con_parametros_da_error(self):
        client = self.loguear_usuario()
        response = client.get(OBTENER_TEMATICAS_MATERIAS, query_string={"parametros": "sdaa"})
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)


if __name__ == '__main__':
    import unittest

    unittest.main()
