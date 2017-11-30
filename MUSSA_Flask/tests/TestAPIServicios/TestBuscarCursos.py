if __name__ == '__main__':
    import os
    import sys
    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase

import app
from app import db
from app.models.horarios_models import Curso, Horario, HorarioPorCurso, CarreraPorCurso
from app.models.carreras_models import Carrera

import json

import datetime

from app.API_Rest.services import *
from app.API_Rest.codes import *

class TestBuscarCursos(TestBase):

    ##########################################################
    ##                   Configuracion                      ##
    ##########################################################

    FECHA = datetime.datetime.now()

    CARRERA_1 = {
        "id": 1,
        "codigo": "10",
        "nombre": 'Ingeniería en Informática',
        "duracion_estimada_en_cuatrimestres": 12,
        "requiere_prueba_suficiencia_de_idioma": False
    }

    CARRERA_2 = {
        "id": 2,
        "codigo": "9",
        "nombre": 'Otra carrera test',
        "duracion_estimada_en_cuatrimestres": 8,
        "requiere_prueba_suficiencia_de_idioma": True
    }

    def get_carreras_bd(self):
        return [self.CARRERA_1, self.CARRERA_2]

    HORARIO_1 = {
        "id": 1,
        "dia": "Lunes",
        "hora_desde": "7.5",
        "hora_hasta": "11",
        "hora_desde_reloj": "07:30",
        "hora_hasta_reloj": "11:00"
    }

    HORARIO_2 = {
        "id": 2,
        "dia": "Jueves",
        "hora_desde": "16",
        "hora_hasta": "21",
        "hora_desde_reloj": "16:00",
        "hora_hasta_reloj": "21:00"
    }

    HORARIO_3 = {
        "id": 3,
        "dia": "Viernes",
        "hora_desde": "7.5",
        "hora_hasta": "13",
        "hora_desde_reloj": "07:30",
        "hora_hasta_reloj": "13:00"
    }

    HORARIO_4 = {
        "id": 4,
        "dia": "Viernes",
        "hora_desde": "7.5",
        "hora_hasta": "13",
        "hora_desde_reloj": "07:30",
        "hora_hasta_reloj": "13:00"
    }

    HORARIO_5 = {
        "id": 5,
        "dia": "Sabados",
        "hora_desde": "7",
        "hora_hasta": "11",
        "hora_desde_reloj": "07:00",
        "hora_hasta_reloj": "11:00"
    }

    def get_horarios_bd(self):
        return [self.HORARIO_1, self.HORARIO_2, self.HORARIO_3, self.HORARIO_4, self.HORARIO_5]

    CURSO_7540_A_DOS_CARRERAS = {
        "id": 1,
        "codigo_materia": "7540",
        "codigo": "7540-CursoA",
        "docentes": "Doc1",
        "se_dicta_primer_cuatrimestre": True,
        "se_dicta_segundo_cuatrimestre": True,
        "cuatrimestre": "Ambos cuatrimestres",
        "cantidad_encuestas_completas": 20,
        "puntaje_total_encuestas": 105,
        "fecha_actualizacion": FECHA,
        "horarios": [HORARIO_1, HORARIO_2],
        "carreras": [CARRERA_1, CARRERA_2]
    }

    CURSO_7540_B_DOS_CARRERAS = {
        "id": 2,
        "codigo_materia": "7540",
        "codigo": "7540-CursoB",
        "docentes": "Doc2",
        "se_dicta_primer_cuatrimestre": True,
        "se_dicta_segundo_cuatrimestre": False,
        "cuatrimestre": "Solo el 1º cuatrimestre",
        "cantidad_encuestas_completas": 0,
        "puntaje_total_encuestas": 0,
        "fecha_actualizacion": FECHA,
        "horarios": [HORARIO_3],
        "carreras": [CARRERA_1, CARRERA_2]
    }

    CURSO_7540_C_UNA_CARRERA = {
        "id": 3,
        "codigo_materia": "7540",
        "codigo": "7540-CursoC",
        "docentes": "Doc2",
        "se_dicta_primer_cuatrimestre": False,
        "se_dicta_segundo_cuatrimestre": True,
        "cuatrimestre": "Solo el 2º cuatrimestre",
        "cantidad_encuestas_completas": 0,
        "puntaje_total_encuestas": 0,
        "fecha_actualizacion": FECHA,
        "horarios": [HORARIO_4, HORARIO_5],
        "carreras": [CARRERA_1]
    }

    CURSO_6680_UNA_CARRERA = {
        "id": 4,
        "codigo_materia": "6680",
        "codigo": "6680-CursoA",
        "docentes": "Doc2",
        "se_dicta_primer_cuatrimestre": True,
        "se_dicta_segundo_cuatrimestre": False,
        "cuatrimestre": "Solo el 1º cuatrimestre",
        "cantidad_encuestas_completas": 0,
        "puntaje_total_encuestas": 0,
        "fecha_actualizacion": FECHA,
        "horarios": [HORARIO_4, HORARIO_5],
        "carreras": [CARRERA_1]
    }

    CURSO_8787_NO_SE_DICTA_NINGUN_CUATRIMESTRE = {
        "id": 5,
        "codigo_materia": "8787",
        "codigo": "8787-CursoA",
        "docentes": "Doc2",
        "se_dicta_primer_cuatrimestre": False,
        "se_dicta_segundo_cuatrimestre": False,
        "cuatrimestre": "No se dicta actualmente",
        "cantidad_encuestas_completas": 0,
        "puntaje_total_encuestas": 0,
        "fecha_actualizacion": FECHA,
        "horarios": [HORARIO_4, HORARIO_5],
        "carreras": [CARRERA_1]
    }

    def get_cursos_bd(self):
        return [self.CURSO_7540_A_DOS_CARRERAS,
                self.CURSO_7540_B_DOS_CARRERAS,
                self.CURSO_7540_C_UNA_CARRERA,
                self.CURSO_6680_UNA_CARRERA,
                self.CURSO_8787_NO_SE_DICTA_NINGUN_CUATRIMESTRE]


    def get_test_name(self):
        return "test_buscar_cursos"


    def crear_datos_bd(self):
        for carrera in self.get_carreras_bd():
            self.agregar_carrera(carrera)

        for horario in self.get_horarios_bd():
            self.agregar_horario(horario)

        for curso in self.get_cursos_bd():
            self.agregar_curso(curso)

            for c_horario in curso["horarios"]:
                self.agregar_horario_por_curso(curso, c_horario)

            for c_carrera in curso["carreras"]:
                self.agregar_carrera_por_curso(curso, c_carrera)


    def agregar_carrera(self, datos):
        db.session.add(Carrera(
            codigo = datos["codigo"],
            nombre = datos["nombre"],
            duracion_estimada_en_cuatrimestres = datos["duracion_estimada_en_cuatrimestres"],
            requiere_prueba_suficiencia_de_idioma = datos["requiere_prueba_suficiencia_de_idioma"]
        ))
        db.session.commit()


    def agregar_curso(self, datos):
        db.session.add(Curso(
            codigo_materia = datos["codigo_materia"],
            codigo = datos["codigo"],
            docentes = datos["docentes"],
            se_dicta_primer_cuatrimestre = datos["se_dicta_primer_cuatrimestre"],
            se_dicta_segundo_cuatrimestre = datos["se_dicta_segundo_cuatrimestre"],
            cantidad_encuestas_completas = datos["cantidad_encuestas_completas"],
            puntaje_total_encuestas = datos["puntaje_total_encuestas"],
            fecha_actualizacion = datos["fecha_actualizacion"],
        ))
        db.session.commit()


    def agregar_horario(self, datos):
        db.session.add(Horario(
            dia = datos["dia"],
            hora_desde = datos["hora_desde"],
            hora_hasta = datos["hora_hasta"]
        ))
        db.session.commit()


    def agregar_horario_por_curso(self, curso, horario):
        db.session.add(HorarioPorCurso(
            curso_id = curso["id"],
            horario_id = horario["id"]
        ))
        db.session.commit()


    def agregar_carrera_por_curso(self, curso, carrera):
        db.session.add(CarreraPorCurso(
            curso_id = curso["id"],
            carrera_id = carrera["id"]
        ))
        db.session.commit()

    ##########################################################
    ##                 Funciones Auxiliares                 ##
    ##########################################################

    def se_encuentra_el_horario(self, horario, l_horarios):
        for l_horario in l_horarios:
            if (horario["dia"] == l_horario["dia"] and
                horario["hora_desde"] == l_horario["hora_desde"] and
                horario["hora_hasta"] == l_horario["hora_hasta"]):
                return True
        return False


    def se_encuentra_la_carrera(self, carrera, l_carreras):
        for l_carrera in l_carreras:
            if (carrera["codigo"] == l_carrera["codigo"] and
                carrera["nombre"] == l_carrera["nombre"]):
                return True
        return False


    def calcular_puntaje(self, curso):
        puntaje = curso["puntaje_total_encuestas"]
        total_encuestas = curso["cantidad_encuestas_completas"]
        if total_encuestas > 0:
            return puntaje / total_encuestas

        return 0

    ##########################################################
    ##                      Tests                           ##
    ##########################################################

    def test_buscar_cursos_sin_parametros_devuelve_todos_los_cursos_que_se_dictan_algun_cuatrimestre(self):
        client = self.app.test_client()
        response = client.get(BUSCAR_CURSOS_SERVICE)
        assert(response.status_code == SUCCESS_OK)

        cursos = json.loads(response.get_data(as_text=True))["cursos"]

        assert(len(cursos) == 4)


    def test_buscar_cursos_con_parametro_filtrar_true_devuelve_todos_los_cursos_que_se_dictan_algun_cuatrimestre(self):
        parametros = {"filtrar_cursos": True}
        client = self.app.test_client()
        response = client.get(BUSCAR_CURSOS_SERVICE, query_string=parametros)
        assert(response.status_code == SUCCESS_OK)

        cursos = json.loads(response.get_data(as_text=True))["cursos"]

        assert(len(cursos) == 4)


    def test_buscar_cursos_con_parametro_filtrar_false_devuelve_todos_los_cursos_auqnue_no_se_dicten_en_ningun_cuatrimestre(self):
        parametros = {"filtrar_cursos": False}
        client = self.app.test_client()
        response = client.get(BUSCAR_CURSOS_SERVICE, query_string=parametros)
        assert(response.status_code == SUCCESS_OK)

        cursos = json.loads(response.get_data(as_text=True))["cursos"]

        assert(len(cursos) == 5)


    def test_buscar_curso_por_id_valido_dictada_ambos_cuatrimestres_devuelve_solo_ese_curso(self):
        parametros = {"id_curso": self.CURSO_7540_A_DOS_CARRERAS["id"]}
        client = self.app.test_client()
        response = client.get(BUSCAR_CURSOS_SERVICE, query_string=parametros)
        assert(response.status_code == SUCCESS_OK)

        cursos = json.loads(response.get_data(as_text=True))["cursos"]

        assert(len(cursos) == 1)

        curso = cursos[0]

        assert(curso["id"] == self.CURSO_7540_A_DOS_CARRERAS["id"])
        assert(curso["codigo_materia"] == self.CURSO_7540_A_DOS_CARRERAS["codigo_materia"])
        assert(curso["codigo_curso"] == self.CURSO_7540_A_DOS_CARRERAS["codigo"])
        assert(curso["docentes"] == self.CURSO_7540_A_DOS_CARRERAS["docentes"])
        assert(curso["se_dicta_primer_cuatri"] == self.CURSO_7540_A_DOS_CARRERAS["se_dicta_primer_cuatrimestre"])
        assert(curso["se_dicta_segundo_cuatri"] == self.CURSO_7540_A_DOS_CARRERAS["se_dicta_segundo_cuatrimestre"])
        assert(curso["puntaje"] == self.calcular_puntaje(self.CURSO_7540_A_DOS_CARRERAS))
        assert(curso["cuatrimestre"] == self.CURSO_7540_A_DOS_CARRERAS["cuatrimestre"])

        horario1 = {
            "dia": self.HORARIO_1["dia"],
            "hora_desde": self.HORARIO_1["hora_desde_reloj"],
            "hora_hasta": self.HORARIO_1["hora_hasta_reloj"]
        }

        assert(self.se_encuentra_el_horario(horario1, curso["horarios"]))

        horario2 = {
            "dia": self.HORARIO_2["dia"],
            "hora_desde": self.HORARIO_2["hora_desde_reloj"],
            "hora_hasta": self.HORARIO_2["hora_hasta_reloj"]
        }

        assert(self.se_encuentra_el_horario(horario2, curso["horarios"]))

        carrera1 = {
            "codigo": self.CARRERA_1["codigo"],
            "nombre": self.CARRERA_1["nombre"]
        }

        assert(self.se_encuentra_la_carrera(carrera1, curso["carreras"]))

        carrera2 = {
            "codigo": self.CARRERA_2["codigo"],
            "nombre": self.CARRERA_2["nombre"]
        }

        assert(self.se_encuentra_la_carrera(carrera2, curso["carreras"]))


    def test_buscar_curso_por_id_valido_que_no_dicta_sin_indicar_filtro_resultados_devuelve_error(self):
        parametros = {"id_curso": self.CURSO_8787_NO_SE_DICTA_NINGUN_CUATRIMESTRE["id"]}
        client = self.app.test_client()
        response = client.get(BUSCAR_CURSOS_SERVICE, query_string=parametros)
        assert(response.status_code == CLIENT_ERROR_BAD_REQUEST)


    def test_buscar_curso_por_id_valido_que_no_dicta_indicando_filtrar_resultados_devuelve_error(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO_8787_NO_SE_DICTA_NINGUN_CUATRIMESTRE["id"]
        parametros["filtrar_cursos"] = True
        client = self.app.test_client()
        response = client.get(BUSCAR_CURSOS_SERVICE, query_string=parametros)
        assert(response.status_code == CLIENT_ERROR_BAD_REQUEST)


    def test_buscar_curso_por_id_valido_que_no_dicta_indicando_no_filtrar_resultados_devuelve_el_curso(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO_8787_NO_SE_DICTA_NINGUN_CUATRIMESTRE["id"]
        parametros["filtrar_cursos"] = False
        client = self.app.test_client()
        response = client.get(BUSCAR_CURSOS_SERVICE, query_string=parametros)
        assert(response.status_code == SUCCESS_OK)

        cursos = json.loads(response.get_data(as_text=True))["cursos"]

        assert(len(cursos) == 1)

        curso = cursos[0]

        assert(curso["id"] == self.CURSO_8787_NO_SE_DICTA_NINGUN_CUATRIMESTRE["id"])
        assert(curso["codigo_materia"] == self.CURSO_8787_NO_SE_DICTA_NINGUN_CUATRIMESTRE["codigo_materia"])
        assert(curso["codigo_curso"] == self.CURSO_8787_NO_SE_DICTA_NINGUN_CUATRIMESTRE["codigo"])
        assert(curso["docentes"] == self.CURSO_8787_NO_SE_DICTA_NINGUN_CUATRIMESTRE["docentes"])
        assert(curso["se_dicta_primer_cuatri"] == self.CURSO_8787_NO_SE_DICTA_NINGUN_CUATRIMESTRE["se_dicta_primer_cuatrimestre"])
        assert(curso["se_dicta_segundo_cuatri"] == self.CURSO_8787_NO_SE_DICTA_NINGUN_CUATRIMESTRE["se_dicta_segundo_cuatrimestre"])
        assert(curso["puntaje"] == self.calcular_puntaje(self.CURSO_8787_NO_SE_DICTA_NINGUN_CUATRIMESTRE))
        assert(curso["cuatrimestre"] == self.CURSO_8787_NO_SE_DICTA_NINGUN_CUATRIMESTRE["cuatrimestre"])

        horario4 = {
            "dia": self.HORARIO_4["dia"],
            "hora_desde": self.HORARIO_4["hora_desde_reloj"],
            "hora_hasta": self.HORARIO_4["hora_hasta_reloj"]
        }

        assert(self.se_encuentra_el_horario(horario4, curso["horarios"]))

        horario5 = {
            "dia": self.HORARIO_5["dia"],
            "hora_desde": self.HORARIO_5["hora_desde_reloj"],
            "hora_hasta": self.HORARIO_5["hora_hasta_reloj"]
        }

        assert(self.se_encuentra_el_horario(horario5, curso["horarios"]))

        carrera1 = {
            "codigo": self.CARRERA_1["codigo"],
            "nombre": self.CARRERA_1["nombre"]
        }

        assert(self.se_encuentra_la_carrera(carrera1, curso["carreras"]))

        #si se busca por id no se le da importancia ni al nombre ni al codigo
        #buscar por nombre
        #buscar por codigo
        #buscar por nombre y codigo
        #filtrar resultados de determiandas carreras
        #pasar parametros erroneos

if __name__ == '__main__':
    import unittest
    unittest.main()