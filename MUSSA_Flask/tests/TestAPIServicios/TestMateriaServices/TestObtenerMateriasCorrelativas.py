if __name__ == '__main__':
    import sys

    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase
from app import db
from app.models.carreras_models import Materia, Carrera, TipoMateria, Correlativas
import json
from app.API_Rest.codes import *


class TestObtenerMateriasCorrelativas(TestBase):
    ##########################################################
    ##                   Configuracion                      ##
    ##########################################################

    ID_SIN_CORRELATIVAS = "1"
    ID_CON_UNA_CORRELATIVA = "2"
    ID_CON_DOS_CORRELATIVAS = "4"

    def get_test_name(self):
        return "test_obtener_materias_correlativas"

    def crear_datos_bd(self):
        carrera = Carrera(
            codigo='10',
            nombre='Ingeniería en Informática',
            duracion_estimada_en_cuatrimestres=12,
            requiere_prueba_suficiencia_de_idioma=False
        )
        db.session.add(carrera)

        carrera2 = Carrera(
            codigo='9',
            nombre='Otra carrera test',
            duracion_estimada_en_cuatrimestres=12,
            requiere_prueba_suficiencia_de_idioma=False
        )
        db.session.add(carrera2)
        db.session.commit()

        tipo = TipoMateria(descripcion="Un tipo")
        db.session.add(tipo)
        db.session.commit()

        db.session.add(Materia(
            codigo="9000",
            nombre="Sin correlativas",
            creditos_minimos_para_cursarla=0,
            creditos=10,
            tipo_materia_id=tipo.id,
            carrera_id=carrera.id
        ))

        materia9032 = Materia(
            codigo="9032",
            nombre="Con una correlativa",
            creditos_minimos_para_cursarla=0,
            creditos=10,
            tipo_materia_id=tipo.id,
            carrera_id=carrera.id
        )
        db.session.add(materia9032)

        materia7090 = Materia(
            codigo="7090",
            nombre="es correlativa de 9032",
            creditos_minimos_para_cursarla=0,
            creditos=10,
            tipo_materia_id=tipo.id,
            carrera_id=carrera.id
        )
        db.session.add(materia7090)

        materia7091 = Materia(
            codigo="7091",
            nombre="Tiene dos correlativas",
            creditos_minimos_para_cursarla=0,
            creditos=10,
            tipo_materia_id=tipo.id,
            carrera_id=carrera.id
        )
        db.session.add(materia7091)

        materia6009 = Materia(
            codigo="6009",
            nombre="Es correlativa de 7091",
            creditos_minimos_para_cursarla=50,
            creditos=100,
            tipo_materia_id=tipo.id,
            carrera_id=carrera.id
        )
        db.session.add(materia6009)

        materia8090 = Materia(
            codigo="8090",
            nombre="Es correlativa de 7091",
            creditos_minimos_para_cursarla=50,
            creditos=100,
            tipo_materia_id=tipo.id,
            carrera_id=carrera2.id
        )
        db.session.add(materia8090)

        db.session.commit()

        db.session.add(Correlativas(
            materia_id=materia9032.id,
            materia_correlativa_id=materia7090.id))

        db.session.add(Correlativas(
            materia_id=materia7091.id,
            materia_correlativa_id=materia6009.id))

        db.session.add(Correlativas(
            materia_id=materia7091.id,
            materia_correlativa_id=materia8090.id))

    ##########################################################
    ##                      Tests                           ##
    ##########################################################

    def test_obtener_materias_correlativas_con_materia_sin_correlativas_devuelve_lista_vacia(self):
        client = self.app.test_client()
        idMateria = self.ID_SIN_CORRELATIVAS
        response = client.get(self.get_url_materias_correlativas(idMateria))
        assert (response.status_code == SUCCESS_OK)

        correlativas = json.loads(response.get_data(as_text=True))["correlativas"]

        assert (len(correlativas) == 0)

    def test_obtener_materias_correlativas_con_materia_con_unica_correlativa_devuelve_lista_de_un_elemento(self):
        client = self.app.test_client()
        idMateria = self.ID_CON_UNA_CORRELATIVA
        response = client.get(self.get_url_materias_correlativas(idMateria))
        assert (response.status_code == SUCCESS_OK)

        correlativas = json.loads(response.get_data(as_text=True))["correlativas"]

        assert (len(correlativas) == 1)
        assert (correlativas[0]["id_materia"] == 3)
        assert (correlativas[0]["codigo"] == "7090")
        assert (correlativas[0]["nombre"] == "es correlativa de 9032")

    def test_obtener_materias_correlativas_con_materia_con_correlativas_devuelve_lista_con_todas_las_correlativas(self):
        client = self.app.test_client()
        idMateria = self.ID_CON_DOS_CORRELATIVAS
        response = client.get(self.get_url_materias_correlativas(idMateria))
        assert (response.status_code == SUCCESS_OK)

        correlativas = json.loads(response.get_data(as_text=True))["correlativas"]

        assert (len(correlativas) == 2)

    def test_obtener_materias_con_id_inexistente_devuelve_error(self):
        client = self.app.test_client()
        idMateria = 72
        response = client.get(self.get_url_materias_correlativas(idMateria))
        assert (response.status_code == CLIENT_ERROR_NOT_FOUND)

    def test_obtener_materias_con_id_invalido_devuelve_error(self):
        client = self.app.test_client()
        idMateria = "7sd2"
        response = client.get(self.get_url_materias_correlativas(idMateria))
        assert (response.status_code == CLIENT_ERROR_NOT_FOUND)


if __name__ == '__main__':
    import unittest

    unittest.main()
