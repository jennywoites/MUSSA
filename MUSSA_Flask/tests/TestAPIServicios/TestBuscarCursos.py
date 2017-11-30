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

    def se_encuentra_el_curso(self, curso_origen, l_cursos):
        for curso_servicio in l_cursos:
            if self.los_cursos_son_iguales(curso_servicio, curso_origen):
                return True

        return False


    def los_cursos_son_iguales(self, curso_servicio, curso_origen):
        if not (curso_origen["id"] == curso_servicio["id"] and
                curso_origen["codigo_materia"] == curso_servicio["codigo_materia"] and
                curso_origen["codigo"] == curso_servicio["codigo_curso"] and
                curso_origen["docentes"] == curso_servicio["docentes"] and
                curso_origen["se_dicta_primer_cuatrimestre"] == curso_servicio["se_dicta_primer_cuatri"] and
                curso_origen["se_dicta_segundo_cuatrimestre"] == curso_servicio["se_dicta_segundo_cuatri"] and
                self.calcular_puntaje(curso_origen) == curso_servicio["puntaje"] and
                curso_origen["cuatrimestre"] == curso_servicio["cuatrimestre"]):
            
            return False

        for horario in curso_origen["horarios"]:
            h = {
                "dia": horario["dia"],
                "hora_desde": horario["hora_desde_reloj"],
                "hora_hasta": horario["hora_hasta_reloj"]
            }
            if not self.se_encuentra_el_horario(h, curso_servicio["horarios"]):
                return False


        for carrera in curso_origen["carreras"]:
            c = {
                "codigo": carrera["codigo"],
                "nombre": carrera["nombre"]
            }
            if not self.se_encuentra_la_carrera(c, curso_servicio["carreras"]):
                return False

        return True


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

        self.se_encuentra_el_curso(self.CURSO_7540_A_DOS_CARRERAS, cursos)


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

        self.se_encuentra_el_curso(self.CURSO_8787_NO_SE_DICTA_NINGUN_CUATRIMESTRE, cursos)


    def test_buscar_curso_por_id_con_codigo_y_nombre_validos_descarta_los_campos_codigo_y_nombre_pero_los_valida(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO_7540_A_DOS_CARRERAS["id"]
        parametros["nombre_curso"] = "589-sm'p"
        parametros["codigo_materia"] = "4875"

        client = self.app.test_client()
        response = client.get(BUSCAR_CURSOS_SERVICE, query_string=parametros)
        assert(response.status_code == SUCCESS_OK)

        cursos = json.loads(response.get_data(as_text=True))["cursos"]

        assert(len(cursos) == 1)

        self.se_encuentra_el_curso(self.CURSO_7540_A_DOS_CARRERAS, cursos)


    def test_buscar_curso_por_id_con_codigo_valido_y_nombre_invalido_descarta_los_campos_codigo_y_nombre_pero_los_valida(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO_7540_A_DOS_CARRERAS["id"]
        parametros["nombre_curso"] = "589-?sm'p"
        parametros["codigo_materia"] = "4875"

        client = self.app.test_client()
        response = client.get(BUSCAR_CURSOS_SERVICE, query_string=parametros)
        assert(response.status_code == CLIENT_ERROR_BAD_REQUEST)


    def test_buscar_curso_por_id_con_codigo_invalido_y_nombre_valido_descarta_los_campos_codigo_y_nombre_pero_los_valida(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO_7540_A_DOS_CARRERAS["id"]
        parametros["nombre_curso"] = "589-sm'p"
        parametros["codigo_materia"] = "487s5"

        client = self.app.test_client()
        response = client.get(BUSCAR_CURSOS_SERVICE, query_string=parametros)
        assert(response.status_code == CLIENT_ERROR_BAD_REQUEST)


    def test_buscar_curso_por_id_con_codigo_y_nombre_invalidos_descarta_los_campos_codigo_y_nombre_pero_los_valida(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO_7540_A_DOS_CARRERAS["id"]
        parametros["nombre_curso"] = "589-sm'p?"
        parametros["codigo_materia"] = "487as5"

        client = self.app.test_client()
        response = client.get(BUSCAR_CURSOS_SERVICE, query_string=parametros)
        assert(response.status_code == CLIENT_ERROR_BAD_REQUEST)


    def test_buscar_curso_por_parte_del_nombre_encuentra_a_todos_los_que_tienen_en_aluna_parte_esos_caracteres_consecutivos(self):
        parametros = {}
        pass
        #buscar por nombre
        #buscar por codigo
        #buscar por nombre y codigo
        #filtrar resultados de determiandas carreras
        #pasar parametros erroneos

if __name__ == '__main__':
    import unittest
    unittest.main()