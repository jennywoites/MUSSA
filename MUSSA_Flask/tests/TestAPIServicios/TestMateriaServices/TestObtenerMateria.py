if __name__ == '__main__':
    import sys

    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase
from app import db
from app.models.carreras_models import Carrera, Materia, TipoMateria
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
        idMateria = 1
        response = client.get(self.get_url_get_materia(idMateria))
        assert (response.status_code == SUCCESS_OK)

        materia = json.loads(response.get_data(as_text=True))

        assert (materia_bdd.id == materia["id_materia"])
        assert (materia_bdd.codigo == materia["codigo"])
        assert (materia_bdd.nombre == materia["nombre"])
        assert (materia_bdd.creditos == materia["creditos"])
        assert (materia_bdd.creditos_minimos_para_cursarla == materia["creditos_minimos_para_cursarla"])
        assert (tipo.descripcion == materia["tipo_materia"])
        assert (tipo.id == materia["tipo_materia_id"])
        assert (carrera.id == materia["carrera_id"])
        assert (carrera.get_descripcion_carrera() == materia["carrera"])

    def test_obtener_materia_con_id_numerico_inexistente_devuelve_error(self):
        client = self.app.test_client()
        idMateria = 10
        response = client.get(self.get_url_get_materia(idMateria))
        assert (response.status_code == CLIENT_ERROR_NOT_FOUND)

    def test_obtener_materia_con_id_invalido_devuelve_not_found_ya_que_no_mapea_con_los_servicios_registrados(self):
        client = self.app.test_client()
        idMateria = "4sd0"
        response = client.get(self.get_url_get_materia(idMateria))
        assert (response.status_code == CLIENT_ERROR_NOT_FOUND)


if __name__ == '__main__':
    import unittest

    unittest.main()
