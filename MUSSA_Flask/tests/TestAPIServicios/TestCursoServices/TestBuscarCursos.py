if __name__ == '__main__':
    import sys

    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase
from app import db
from app.models.horarios_models import Curso, Horario, HorarioPorCurso, CarreraPorCurso
from app.models.carreras_models import Materia, TipoMateria
from app.models.docentes_models import Docente, CursosDocente
import json
import datetime
from app.API_Rest.codes import *
from tests.TestAPIServicios.DAOMock.CarreraDAOMock import CarreraDAOMock, LICENCIATURA_EN_SISTEMAS_1986, \
    INGENIERIA_EN_INFORMATICA_1986


class TestBuscarCursos(TestBase):
    ##########################################################
    ##                   Configuracion                      ##
    ##########################################################

    FECHA = datetime.datetime.now()

    def get_materias_bd(self):
        return [self.MATERIA_7540, self.MATERIA_7540_2, self.MATERIA_7541, self.MATERIA_8787]

    MATERIA_7540 = {
        "codigo": "7540",
        "nombre": "Algoritmos",
        "carrera_id": 1
    }

    MATERIA_7540_2 = {
        "codigo": "7540",
        "nombre": "Algoritmos",
        "carrera_id": 2
    }

    MATERIA_7541 = {
        "codigo": "7541",
        "nombre": "Otra materia",
        "carrera_id": 1
    }

    MATERIA_8787 = {
        "codigo": "8787",
        "nombre": "Otra materia",
        "carrera_id": 2
    }

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

    DOCENTE_1 = {
        "id": 1,
        "nombre_completo": "Woites, Jennifer",
        "nombre": "Jennifer",
        "apellido": "Woites"
    }

    DOCENTE_2 = {
        "id": 2,
        "nombre_completo": "Riesgo, Daniela",
        "nombre": "Daniela",
        "apellido": "Riesgo"
    }

    DOCENTE_3 = {
        "id": 3,
        "nombre_completo": "Wachenchauzer",
        "nombre": "",
        "apellido": "Wachenchauzer"
    }

    DOCENTE_4 = {
        "id": 4,
        "nombre_completo": "Soto, Daniela",
        "nombre": "Daniela",
        "apellido": "Soto"
    }

    DOCENTE_5 = {
        "id": 5,
        "nombre_completo": "Wainer, Ariel",
        "nombre": "Ariel",
        "apellido": "Wainer"
    }

    DOCENTE_6 = {
        "id": 6,
        "nombre_completo": "Essaya, Diego",
        "nombre": "Diego",
        "apellido": "Essaya"
    }

    def get_docentes(self):
        return [self.DOCENTE_1,
                self.DOCENTE_2,
                self.DOCENTE_3,
                self.DOCENTE_4,
                self.DOCENTE_5,
                self.DOCENTE_6]

    CURSO_7540_A_DOS_CARRERAS = {
        "id": 1,
        "codigo_materia": "7540",
        "codigo": "7540-CursoA",
        "docentes": [DOCENTE_1, DOCENTE_2],
        "se_dicta_primer_cuatrimestre": True,
        "se_dicta_segundo_cuatrimestre": True,
        "cuatrimestre": "Ambos cuatrimestres",
        "cantidad_encuestas_completas": 20,
        "puntaje_total_encuestas": 105,
        "fecha_actualizacion": FECHA,
        "horarios": [HORARIO_1, HORARIO_2],
        "carreras": [LICENCIATURA_EN_SISTEMAS_1986, INGENIERIA_EN_INFORMATICA_1986]
    }

    CURSO_7540_B_DOS_CARRERAS = {
        "id": 2,
        "codigo_materia": "7540",
        "codigo": "7540-CursoB",
        "docentes": [DOCENTE_3],
        "se_dicta_primer_cuatrimestre": True,
        "se_dicta_segundo_cuatrimestre": False,
        "cuatrimestre": "Solo el 1º cuatrimestre",
        "cantidad_encuestas_completas": 0,
        "puntaje_total_encuestas": 0,
        "fecha_actualizacion": FECHA,
        "horarios": [HORARIO_3],
        "carreras": [LICENCIATURA_EN_SISTEMAS_1986, INGENIERIA_EN_INFORMATICA_1986]
    }

    CURSO_7540_C_UNA_CARRERA = {
        "id": 3,
        "codigo_materia": "7540",
        "codigo": "7540-CursoC",
        "docentes": [DOCENTE_4],
        "se_dicta_primer_cuatrimestre": False,
        "se_dicta_segundo_cuatrimestre": True,
        "cuatrimestre": "Solo el 2º cuatrimestre",
        "cantidad_encuestas_completas": 0,
        "puntaje_total_encuestas": 0,
        "fecha_actualizacion": FECHA,
        "horarios": [HORARIO_4, HORARIO_5],
        "carreras": [INGENIERIA_EN_INFORMATICA_1986]
    }

    CURSO_7541_UNA_CARRERA = {
        "id": 4,
        "codigo_materia": "7541",
        "codigo": "7541-CursoA",
        "docentes": [DOCENTE_5, DOCENTE_1],
        "se_dicta_primer_cuatrimestre": True,
        "se_dicta_segundo_cuatrimestre": False,
        "cuatrimestre": "Solo el 1º cuatrimestre",
        "cantidad_encuestas_completas": 0,
        "puntaje_total_encuestas": 0,
        "fecha_actualizacion": FECHA,
        "horarios": [HORARIO_4, HORARIO_5],
        "carreras": [INGENIERIA_EN_INFORMATICA_1986]
    }

    CURSO_8787_NO_SE_DICTA_NINGUN_CUATRIMESTRE = {
        "id": 5,
        "codigo_materia": "8787",
        "codigo": "8787-CursoA",
        "docentes": [DOCENTE_6],
        "se_dicta_primer_cuatrimestre": False,
        "se_dicta_segundo_cuatrimestre": False,
        "cuatrimestre": "No se dicta actualmente",
        "cantidad_encuestas_completas": 0,
        "puntaje_total_encuestas": 0,
        "fecha_actualizacion": FECHA,
        "horarios": [HORARIO_4, HORARIO_5],
        "carreras": [LICENCIATURA_EN_SISTEMAS_1986]
    }

    def get_cursos_bd(self):
        return [self.CURSO_7540_A_DOS_CARRERAS,
                self.CURSO_7540_B_DOS_CARRERAS,
                self.CURSO_7540_C_UNA_CARRERA,
                self.CURSO_7541_UNA_CARRERA,
                self.CURSO_8787_NO_SE_DICTA_NINGUN_CUATRIMESTRE]

    def get_test_name(self):
        return "test_buscar_cursos"

    def crear_datos_bd(self):
        carrerasDAO = CarreraDAOMock()
        carrerasDAO.crear_licenciatura_en_sistemas_1986()
        carrerasDAO.crear_ingenieria_informatica_1986()

        for materia in self.get_materias_bd():
            self.agregar_materia(materia)

        for docente in self.get_docentes():
            self.agregar_docente(docente)

        for horario in self.get_horarios_bd():
            self.agregar_horario(horario)

        for curso in self.get_cursos_bd():
            self.agregar_curso(curso)

            for c_horario in curso["horarios"]:
                self.agregar_horario_por_curso(curso, c_horario)

            for c_carrera in curso["carreras"]:
                self.agregar_carrera_por_curso(curso, c_carrera)

    def agregar_docente(self, docente):
        db.session.add(Docente(
            apellido=docente["apellido"],
            nombre=docente["nombre"]
        ))
        db.session.commit()

    def agregar_materia(self, datos):
        tipo_materia = TipoMateria.query.first()
        if not tipo_materia:
            tipo_materia = TipoMateria(descripcion="fruta")
            db.session.add(tipo_materia)
            db.session.commit()

        db.session.add(Materia(
            codigo=datos["codigo"],
            nombre=datos["nombre"],
            objetivos="",
            creditos_minimos_para_cursarla=0,
            creditos=0,
            tipo_materia_id=tipo_materia.id,
            carrera_id=datos["carrera_id"]
        ))

    def agregar_curso(self, datos):
        curso = Curso(
            codigo_materia=datos["codigo_materia"],
            codigo=datos["codigo"],
            se_dicta_primer_cuatrimestre=datos["se_dicta_primer_cuatrimestre"],
            se_dicta_segundo_cuatrimestre=datos["se_dicta_segundo_cuatrimestre"],
            cantidad_encuestas_completas=datos["cantidad_encuestas_completas"],
            puntaje_total_encuestas=datos["puntaje_total_encuestas"],
            fecha_actualizacion=datos["fecha_actualizacion"],
        )
        db.session.add(curso)
        db.session.commit()

        for docente in datos["docentes"]:
            db.session.add(CursosDocente(
                curso_id=curso.id,
                docente_id=docente["id"]
            ))
        db.session.commit()

    def agregar_horario(self, datos):
        db.session.add(Horario(
            dia=datos["dia"],
            hora_desde=datos["hora_desde"],
            hora_hasta=datos["hora_hasta"]
        ))
        db.session.commit()

    def agregar_horario_por_curso(self, curso, horario):
        db.session.add(HorarioPorCurso(
            curso_id=curso["id"],
            horario_id=horario["id"]
        ))
        db.session.commit()

    def agregar_carrera_por_curso(self, curso, carrera):
        db.session.add(CarreraPorCurso(
            curso_id=curso["id"],
            carrera_id=carrera["id"]
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
        if not (curso_origen["id"] == curso_servicio["id_curso"] and
                        curso_origen["codigo_materia"] == curso_servicio["codigo_materia"] and
                        curso_origen["codigo"] == curso_servicio["codigo_curso"] and
                    self.los_docentes_coinciden(curso_origen, curso_servicio) and
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

    def los_docentes_coinciden(self, curso_origen, curso_servicio):
        nombres = []
        for docente in curso_origen["docentes"]:
            nombres.append(docente["nombre_completo"])

        nombres_servicio = curso_servicio["docentes"].split("-")
        if not len(nombres) == len(nombres_servicio):
            return False

        for nombre in nombres_servicio:
            if nombre not in nombres:
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
            return "{0:.2f}".format(puntaje / total_encuestas)
        return 0

    ##########################################################
    ##                      Tests                           ##
    ##########################################################

    def test_buscar_cursos_sin_parametros_devuelve_todos_los_cursos_se_dicten_o_no(self):
        client = self.app.test_client()
        response = client.get(self.get_url_all_cursos())
        assert (response.status_code == SUCCESS_OK)

        cursos = json.loads(response.get_data(as_text=True))["cursos"]

        assert (len(cursos) == 5)

    def test_buscar_cursos_con_parametro_filtrar_true_devuelve_todos_los_cursos_que_se_dictan_algun_cuatrimestre(self):
        parametros = {"filtrar_cursos": True}
        client = self.app.test_client()
        response = client.get(self.get_url_all_cursos(), query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        cursos = json.loads(response.get_data(as_text=True))["cursos"]

        assert (len(cursos) == 4)

    def test_buscar_cursos_con_parametro_filtrar_false_devuelve_todos_los_cursos_auqnue_no_se_dicten_en_ningun_cuatrimestre(
            self):
        parametros = {"filtrar_cursos": False}
        client = self.app.test_client()
        response = client.get(self.get_url_all_cursos(), query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        cursos = json.loads(response.get_data(as_text=True))["cursos"]

        assert (len(cursos) == 5)

    def test_buscar_curso_por_parte_del_nombre_del_medio_encuentra_a_todos_los_que_tienen_en_alguna_parte_esos_caracteres_consecutivos(
            self):
        parametros = {}
        parametros["nombre_curso"] = "-Curso"

        client = self.app.test_client()
        response = client.get(self.get_url_all_cursos(), query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        cursos = json.loads(response.get_data(as_text=True))["cursos"]

        assert (len(cursos) == 5)

        self.se_encuentra_el_curso(self.CURSO_7540_A_DOS_CARRERAS, cursos)
        self.se_encuentra_el_curso(self.CURSO_7540_B_DOS_CARRERAS, cursos)
        self.se_encuentra_el_curso(self.CURSO_7540_C_UNA_CARRERA, cursos)
        self.se_encuentra_el_curso(self.CURSO_7541_UNA_CARRERA, cursos)
        self.se_encuentra_el_curso(self.CURSO_8787_NO_SE_DICTA_NINGUN_CUATRIMESTRE, cursos)

    def test_buscar_curso_por_parte_del_nombre_del_medio_y_no_filtrar_cursos_encuentra_a_todos_los_que_tienen_en_alguna_parte_esos_caracteres_consecutivos(
            self):
        parametros = {}
        parametros["nombre_curso"] = "-Curso"
        parametros["filtrar_cursos"] = False

        client = self.app.test_client()
        response = client.get(self.get_url_all_cursos(), query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        cursos = json.loads(response.get_data(as_text=True))["cursos"]

        assert (len(cursos) == 5)

        self.se_encuentra_el_curso(self.CURSO_7540_A_DOS_CARRERAS, cursos)
        self.se_encuentra_el_curso(self.CURSO_7540_B_DOS_CARRERAS, cursos)
        self.se_encuentra_el_curso(self.CURSO_7540_C_UNA_CARRERA, cursos)
        self.se_encuentra_el_curso(self.CURSO_7541_UNA_CARRERA, cursos)
        self.se_encuentra_el_curso(self.CURSO_8787_NO_SE_DICTA_NINGUN_CUATRIMESTRE, cursos)

    def test_buscar_curso_por_parte_del_nombre_comienza_con_encuentra_a_todos_los_que_tienen_en_aluna_parte_esos_caracteres_consecutivos(
            self):
        parametros = {}
        parametros["nombre_curso"] = "7540-Curso"

        client = self.app.test_client()
        response = client.get(self.get_url_all_cursos(), query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        cursos = json.loads(response.get_data(as_text=True))["cursos"]

        assert (len(cursos) == 3)

        self.se_encuentra_el_curso(self.CURSO_7540_A_DOS_CARRERAS, cursos)
        self.se_encuentra_el_curso(self.CURSO_7540_B_DOS_CARRERAS, cursos)
        self.se_encuentra_el_curso(self.CURSO_7540_C_UNA_CARRERA, cursos)

    def test_buscar_por_nombre_invalido_por_longitud_devuelve_error(self):
        parametros = {}
        parametros["nombre_curso"] = "456789123456safassaffassfa"

        client = self.app.test_client()
        response = client.get(self.get_url_all_cursos(), query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_buscar_por_nombre_valido_no_existente_devuelve_lista_vacia(self):
        parametros = {}
        parametros["nombre_curso"] = "zzzzzz"

        client = self.app.test_client()
        response = client.get(self.get_url_all_cursos(), query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        cursos = json.loads(response.get_data(as_text=True))["cursos"]

        assert (len(cursos) == 0)

    def test_buscar_por_parte_del_codigo_devuelve_todos_los_que_comienzan_con_ese_numero(self):
        parametros = {}
        parametros["codigo_materia"] = "754"

        client = self.app.test_client()
        response = client.get(self.get_url_all_cursos(), query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        cursos = json.loads(response.get_data(as_text=True))["cursos"]

        assert (len(cursos) == 4)

        self.se_encuentra_el_curso(self.CURSO_7540_A_DOS_CARRERAS, cursos)
        self.se_encuentra_el_curso(self.CURSO_7540_B_DOS_CARRERAS, cursos)
        self.se_encuentra_el_curso(self.CURSO_7540_C_UNA_CARRERA, cursos)
        self.se_encuentra_el_curso(self.CURSO_7541_UNA_CARRERA, cursos)

    def test_buscar_por_codigo_completo_todos_los_que_tiene_ese_codigo(self):
        parametros = {}
        parametros["codigo_materia"] = "7540"

        client = self.app.test_client()
        response = client.get(self.get_url_all_cursos(), query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        cursos = json.loads(response.get_data(as_text=True))["cursos"]

        assert (len(cursos) == 3)

        self.se_encuentra_el_curso(self.CURSO_7540_A_DOS_CARRERAS, cursos)
        self.se_encuentra_el_curso(self.CURSO_7540_B_DOS_CARRERAS, cursos)
        self.se_encuentra_el_curso(self.CURSO_7540_C_UNA_CARRERA, cursos)

    def test_buscar_por_codigo_valido_no_existente_da_error(self):
        parametros = {}
        parametros["codigo_materia"] = "9999"

        client = self.app.test_client()
        response = client.get(self.get_url_all_cursos(), query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_NOT_FOUND)

    def test_buscar_por_codigo_invalido_da_error(self):
        parametros = {}
        parametros["codigo_materia"] = "589-asmp"

        client = self.app.test_client()
        response = client.get(self.get_url_all_cursos(), query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_buscar_por_codigo_completo_y_nombre_todos_los_que_tiene_ese_codigo_y_esa_parte_del_nombre_en_el(self):
        parametros = {}
        parametros["codigo_materia"] = "754"
        parametros["nombre_curso"] = "-Curso"

        client = self.app.test_client()
        response = client.get(self.get_url_all_cursos(), query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        cursos = json.loads(response.get_data(as_text=True))["cursos"]

        assert (len(cursos) == 4)

        self.se_encuentra_el_curso(self.CURSO_7540_A_DOS_CARRERAS, cursos)
        self.se_encuentra_el_curso(self.CURSO_7540_B_DOS_CARRERAS, cursos)
        self.se_encuentra_el_curso(self.CURSO_7540_C_UNA_CARRERA, cursos)
        self.se_encuentra_el_curso(self.CURSO_7541_UNA_CARRERA, cursos)

    def test_buscar_todos_los_cursos_cuya_carrera_sea_la_especificada_filtrando_resultados(self):
        parametros = {}
        parametros["id_carrera"] = LICENCIATURA_EN_SISTEMAS_1986["id"]
        parametros["filtrar_cursos"] = True

        client = self.app.test_client()
        response = client.get(self.get_url_all_cursos(), query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        cursos = json.loads(response.get_data(as_text=True))["cursos"]

        assert (len(cursos) == 2)

        self.se_encuentra_el_curso(self.CURSO_7540_A_DOS_CARRERAS, cursos)
        self.se_encuentra_el_curso(self.CURSO_7540_B_DOS_CARRERAS, cursos)

    def test_buscar_todos_los_cursos_cuya_carrera_sea_la_especificada_sin_filtrar_cursos(self):
        parametros = {}
        parametros["id_carrera"] = LICENCIATURA_EN_SISTEMAS_1986["id"]
        parametros["filtrar_cursos"] = False

        client = self.app.test_client()
        response = client.get(self.get_url_all_cursos(), query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        cursos = json.loads(response.get_data(as_text=True))["cursos"]

        assert (len(cursos) == 3)

        self.se_encuentra_el_curso(self.CURSO_7540_A_DOS_CARRERAS, cursos)
        self.se_encuentra_el_curso(self.CURSO_7540_B_DOS_CARRERAS, cursos)
        self.se_encuentra_el_curso(self.CURSO_8787_NO_SE_DICTA_NINGUN_CUATRIMESTRE, cursos)

    def test_buscar_todos_los_cursos_cuya_carrera_sea_la_especificada_y_su_codigo_coincida_con_el_buscado(self):
        parametros = {}
        parametros["codigo_materia"] = "754"
        parametros["id_carrera"] = INGENIERIA_EN_INFORMATICA_1986["id"]

        client = self.app.test_client()
        response = client.get(self.get_url_all_cursos(), query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        cursos = json.loads(response.get_data(as_text=True))["cursos"]

        assert (len(cursos) == 4)

        self.se_encuentra_el_curso(self.CURSO_7540_A_DOS_CARRERAS, cursos)
        self.se_encuentra_el_curso(self.CURSO_7540_B_DOS_CARRERAS, cursos)
        self.se_encuentra_el_curso(self.CURSO_7540_C_UNA_CARRERA, cursos)
        self.se_encuentra_el_curso(self.CURSO_7541_UNA_CARRERA, cursos)

    def test_buscar_con_carrera_invalida_compuesta_por_carreras_validas(self):
        parametros = {}
        parametros["id_carrera"] = str(LICENCIATURA_EN_SISTEMAS_1986["id"]) + ";" + str(
            INGENIERIA_EN_INFORMATICA_1986["id"])

        client = self.app.test_client()
        response = client.get(self.get_url_all_cursos(), query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_buscar_con_carrera_invalida(self):
        parametros = {}
        parametros["id_carrera"] = "52a"

        client = self.app.test_client()
        response = client.get(self.get_url_all_cursos(), query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_buscar_con_carrera_inexistente(self):
        parametros = {}
        parametros["id_carrera"] = "52"

        client = self.app.test_client()
        response = client.get(self.get_url_all_cursos(), query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_NOT_FOUND)


if __name__ == '__main__':
    import unittest

    unittest.main()
