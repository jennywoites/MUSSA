if __name__ == '__main__':
    import os
    import sys
    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase

import app
from app import db
from app.models.carreras_models import Materia, Carrera, TipoMateria

from app.API_Rest.services import *

class TestBuscarMaterias(TestBase):

    ##########################################################
    ##                   Configuracion                      ##
    ##########################################################

    def get_test_name(self):
        return "test_buscar_materias"


    def crear_datos_bd(self):
        carrera = Carrera(
            codigo = '10',
            nombre = 'Ingeniería en Informática',
            duracion_estimada_en_cuatrimestres = 12,
            requiere_prueba_suficiencia_de_idioma = False
        )
        db.session.add(carrera)

        carrera2 = Carrera(
            codigo = '9',
            nombre = 'Otra carrera test',
            duracion_estimada_en_cuatrimestres = 12,
            requiere_prueba_suficiencia_de_idioma = False
        )
        db.session.add(carrera2)
        db.session.commit()

        tipo = TipoMateria(descripcion="Un tipo")
        db.session.add(tipo)
        db.session.commit()

        db.session.add(Materia(
            codigo = "9000",
            nombre = "AAAAA",
            creditos_minimos_para_cursarla = 0,
            creditos = 10,
            tipo_materia_id = tipo.id,
            carrera_id = carrera.id
        ))

        db.session.add(Materia(
            codigo = "9032",
            nombre = "Materia 2",
            creditos_minimos_para_cursarla = 0,
            creditos = 10,
            tipo_materia_id = tipo.id,
            carrera_id = carrera.id
        ))

        db.session.add(Materia(
            codigo = "7090",
            nombre = "Se llaman iguales",
            creditos_minimos_para_cursarla = 0,
            creditos = 10,
            tipo_materia_id = tipo.id,
            carrera_id = carrera.id
        ))

        db.session.add(Materia(
            codigo = "7091",
            nombre = "Se llaman iguales",
            creditos_minimos_para_cursarla = 0,
            creditos = 10,
            tipo_materia_id = tipo.id,
            carrera_id = carrera.id
        ))

        db.session.add(Materia(
            codigo = "6009",
            nombre = "BBBB",
            creditos_minimos_para_cursarla = 50,
            creditos = 100,
            tipo_materia_id = tipo.id,
            carrera_id = carrera.id
        ))

        db.session.add(Materia(
            codigo = "8090",
            nombre = "CCCC",
            creditos_minimos_para_cursarla = 50,
            creditos = 100,
            tipo_materia_id = tipo.id,
            carrera_id = carrera2.id
        ))

    ##########################################################
    ##                      Tests                           ##
    ##########################################################

    def test_buscar_materias_sin_parametros_devuelve_todas_las_materias(self):
        materias_bdd = Materia.query.all()

        client = self.app.test_client()
        response = client.get(BUSCAR_MATERIAS_SERVICE)
        assert(response.status_code==200)

        materias = response.json["materias"]

        assert(len(materias_bdd) == len(materias))


    def test_buscar_materias_por_codigo_devuelve_todas_las_que_comienzan_con_ese_codigo(self):
        parametros = {}
        parametros["codigo"] = "90"

        client = self.app.test_client()
        response = client.get(BUSCAR_MATERIAS_SERVICE, query_string=parametros)
        assert(response.status_code==200)

        materias = response.json["materias"]

        assert(len(materias) == 2)

        for materia in materias:
            assert(materia["codigo"] in ["9000", "9032"])


    def test_buscar_materias_por_codigo_completo_devuelve_unica_materia(self):
        CODIGO = "9000"
        materia_bdd = Materia.query.filter_by(codigo=CODIGO).first()

        parametros = {}
        parametros["codigo"] = CODIGO

        client = self.app.test_client()
        response = client.get(BUSCAR_MATERIAS_SERVICE, query_string=parametros)
        assert(response.status_code==200)

        materias = response.json["materias"]

        assert(len(materias) == 1)

        materia = materias[0]

        assert(materia["id"] == materia_bdd.id)
        assert(materia["codigo"] == CODIGO)
        assert(materia["nombre"] == "AAAAA")
        assert(materia["carrera"] == 'Ingeniería en Informática')


    def test_buscar_materias_por_texto_no_reconoce_minusculas_o_mayusculas(self):
        TEXTO = "a"
        parametros = {}
        parametros["nombre"] = TEXTO

        client = self.app.test_client()
        response = client.get(BUSCAR_MATERIAS_SERVICE, query_string=parametros)
        assert(response.status_code==200)

        materias = response.json["materias"]

        assert(len(materias) == 4)

        for materia in materias:
            assert(TEXTO.upper() in materia["nombre"].upper())


    def test_buscar_materias_por_texto_y_codigo_trae_el_resultado_que_cumple_ambas_caracteristicas(self):
        CODIGO = "7090"
        TEXTO = "Se llaman iguales"

        parametros = {}
        parametros["nombre"] = TEXTO
        parametros["codigo"] = CODIGO

        client = self.app.test_client()
        response = client.get(BUSCAR_MATERIAS_SERVICE, query_string=parametros)
        assert(response.status_code==200)

        materias = response.json["materias"]

        assert(len(materias) == 1)

        materia = materias[0]
        assert(materia["codigo"] == CODIGO)
        assert(materia["nombre"] == TEXTO)
        assert(materia["carrera"] == 'Ingeniería en Informática')


    def test_buscar_materias_por_carreras_ingenieria_trae_solo_las_de_la_carrera_correspondiente(self):
        parametros = {}
        parametros["carreras"] = "10"

        client = self.app.test_client()
        response = client.get(BUSCAR_MATERIAS_SERVICE, query_string=parametros)
        assert(response.status_code==200)

        materias = response.json["materias"]

        assert(len(materias) == 5)

        for materia in materias:
            assert(materia["carrera"] == 'Ingeniería en Informática')


    def test_buscar_materias_por_carreras_otra_carrera_test_trae_solo_las_de_la_carrera_correspondiente(self):
        parametros = {}
        parametros["carreras"] = "9"

        client = self.app.test_client()
        response = client.get(BUSCAR_MATERIAS_SERVICE, query_string=parametros)
        assert(response.status_code==200)

        materias = response.json["materias"]

        assert(len(materias) == 1)

        for materia in materias:
            assert(materia["carrera"] == 'Otra carrera test')


    def test_buscar_carreras_con_filtro_de_todas_las_carreras_trae_todas_las_materias(self):
        parametros = {}
        parametros["carreras"] = "9,10"

        client = self.app.test_client()
        response = client.get(BUSCAR_MATERIAS_SERVICE, query_string=parametros)
        assert(response.status_code==200)

        materias = response.json["materias"]

        assert(len(materias) == 6)


    def test_buscar_materias_con_carreras_inexistentes_devuelve_bad_request(self):
        parametros = {}
        parametros["carreras"] = "9,10,56"

        client = self.app.test_client()
        response = client.get(BUSCAR_CARRERAS_SERVICE, query_string=parametros)
        assert(response.status_code==400)


    def test_buscar_materias_con_carreras_existentes_y_mal_separador_devuelve_bad_request(self):
        parametros = {}
        parametros["carreras"] = "9-10"

        client = self.app.test_client()
        response = client.get(BUSCAR_CARRERAS_SERVICE, query_string=parametros)
        assert(response.status_code==400)


    def test_buscar_materias_con_codigo_no_numerico_devuelve_bad_request(self):
        parametros = {}
        parametros["codigo"] = "89a"

        client = self.app.test_client()
        response = client.get(BUSCAR_CARRERAS_SERVICE, query_string=parametros)
        assert(response.status_code==400)


    def test_buscar_materias_con_codigo_numerico_muy_largo_devuelve_bad_request(self):
        parametros = {}
        parametros["codigo"] = "89899"

        client = self.app.test_client()
        response = client.get(BUSCAR_CARRERAS_SERVICE, query_string=parametros)
        assert(response.status_code==400)


    def test_buscar_materias_con_nombre_materia_con_numeros_devuelve_bad_request(self):
        parametros = {}
        parametros["nombre"] = "8asf98sfafs9sfafsa9"

        client = self.app.test_client()
        response = client.get(BUSCAR_CARRERAS_SERVICE, query_string=parametros)
        assert(response.status_code==400)


    def test_buscar_materias_con_nombre_materia_con_simbolos_devuelve_bad_request(self):
        parametros = {}
        parametros["nombre"] = "./adjkjad../jjkadk../"

        client = self.app.test_client()
        response = client.get(BUSCAR_CARRERAS_SERVICE, query_string=parametros)
        assert(response.status_code==400)


if __name__ == '__main__':
    import unittest
    unittest.main()