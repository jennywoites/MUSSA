if __name__ == '__main__':
    import sys

    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase

from app import db
from app.models.horarios_models import Curso, Horario, HorarioPorCurso, CarreraPorCurso
from app.models.carreras_models import Carrera, TipoMateria, Materia
from app.models.docentes_models import CursosDocente, Docente

import json

import datetime

from app.API_Rest.services import *
from app.API_Rest.codes import *


class TestObtenerDocentes(TestBase):
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

    def get_carreras_bd(self):
        return [self.CARRERA_1]

    HORARIO_1 = {
        "id": 1,
        "dia": "Lunes",
        "hora_desde": "7.5",
        "hora_hasta": "11",
        "hora_desde_reloj": "07:30",
        "hora_hasta_reloj": "11:00"
    }

    def get_horarios_bd(self):
        return [self.HORARIO_1]

    CURSO = {
        "id": 1,
        "codigo_materia": "7540",
        "codigo": "7540-CursoA",
        "se_dicta_primer_cuatrimestre": True,
        "se_dicta_segundo_cuatrimestre": True,
        "cuatrimestre": "Ambos cuatrimestres",
        "cantidad_encuestas_completas": 20,
        "puntaje_total_encuestas": 105,
        "fecha_actualizacion": FECHA,
        "horarios": [HORARIO_1],
        "carreras": [CARRERA_1]
    }

    def get_cursos_bd(self):
        return [self.CURSO]

    DOCENTE_CON_NOMBRE = {
        "id": 1,
        "apellido": "Woites",
        "nombre": "Jennifer",
        "nombre_completo": "Woites, Jennifer",
        "materias_que_dicta": {
            "7540": "Materia test"
        }
    }

    DOCENTE_SIN_NOMBRE = {
        "id": 2,
        "apellido": "Wainer",
        "nombre": "",
        "nombre_completo": "Wainer",
        "materias_que_dicta": {
            "7540": "Materia test"
        }
    }

    def get_docentes(self):
        return [self.DOCENTE_CON_NOMBRE, self.DOCENTE_SIN_NOMBRE]

    def get_test_name(self):
        return "test_obtener_docentes"

    def crear_datos_bd(self):
        for carrera in self.get_carreras_bd():
            self.agregar_carrera(carrera)

        self.agregar_materia()

        for horario in self.get_horarios_bd():
            self.agregar_horario(horario)

        for curso in self.get_cursos_bd():
            self.agregar_curso(curso)

            for docente in self.get_docentes():
                self.agregar_docente_al_curso(docente, curso)

            for c_horario in curso["horarios"]:
                self.agregar_horario_por_curso(curso, c_horario)

            for c_carrera in curso["carreras"]:
                self.agregar_carrera_por_curso(curso, c_carrera)

    def agregar_materia(self):
        tipo_materia = TipoMateria(descripcion="Tipo Materia Test")
        db.session.add(tipo_materia)
        db.session.commit()

        db.session.add(Materia(
            codigo=self.CURSO["codigo_materia"],
            nombre="Materia test",
            objetivos="Ninguno",
            creditos_minimos_para_cursarla=10,
            creditos=24,
            tipo_materia_id=tipo_materia.id,
            carrera_id=self.CARRERA_1["id"]
        ))

    def agregar_docente_al_curso(self, docente, curso):
        doc = Docente(apellido=docente["apellido"], nombre=docente["nombre"])
        db.session.add(doc)
        db.session.commit()

        db.session.add(CursosDocente(
            docente_id=doc.id,
            curso_id=curso["id"]
        ))
        db.session.commit()

    def agregar_carrera(self, datos):
        db.session.add(Carrera(
            codigo=datos["codigo"],
            nombre=datos["nombre"],
            duracion_estimada_en_cuatrimestres=datos["duracion_estimada_en_cuatrimestres"],
            requiere_prueba_suficiencia_de_idioma=datos["requiere_prueba_suficiencia_de_idioma"]
        ))
        db.session.commit()

    def agregar_curso(self, datos):
        db.session.add(Curso(
            codigo_materia=datos["codigo_materia"],
            codigo=datos["codigo"],
            se_dicta_primer_cuatrimestre=datos["se_dicta_primer_cuatrimestre"],
            se_dicta_segundo_cuatrimestre=datos["se_dicta_segundo_cuatrimestre"],
            cantidad_encuestas_completas=datos["cantidad_encuestas_completas"],
            puntaje_total_encuestas=datos["puntaje_total_encuestas"],
            fecha_actualizacion=datos["fecha_actualizacion"],
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

    def se_encuentra_el_docente(self, docente_origen, l_docentes):
        for docente_servicio in l_docentes:
            if self.los_docentes_son_iguales(docente_servicio, docente_origen):
                return True

        return False

    def los_docentes_son_iguales(self, docente_servicio, docente_origen):
        return (docente_servicio["id_docente"] == docente_origen["id"] and
                docente_servicio["apellido"] == docente_origen["apellido"] and
                docente_servicio["nombre"] == docente_origen["nombre"] and
                docente_servicio["nombre_completo"] == docente_origen["nombre_completo"] and
                self.dictan_las_mismas_materias(docente_origen, docente_servicio))

    def dictan_las_mismas_materias(self, docente_origen, docente_servicio):
        for cod_materia_servicio in docente_servicio["materias_que_dicta"]:
            if not cod_materia_servicio in docente_origen["materias_que_dicta"]:
                return False
            if (docente_origen["materias_que_dicta"][cod_materia_servicio] !=
                    docente_servicio["materias_que_dicta"][cod_materia_servicio]):
                return False

        return len(docente_servicio["materias_que_dicta"]) == len(docente_origen["materias_que_dicta"])

    ##########################################################
    ##                      Tests                           ##
    ##########################################################

    def test_obtener_los_docentes_con_parametros_da_error(self):
        client = self.app.test_client()
        parametros = {}
        parametros["nombre_param"] = "a45d5"
        response = client.get(OBTENER_DOCENTES_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_obtener_los_docentes_devuelve_todos_los_docentes(self):
        client = self.app.test_client()
        response = client.get(OBTENER_DOCENTES_SERVICE)
        assert (response.status_code == SUCCESS_OK)

        docentes = json.loads(response.get_data(as_text=True))["docentes"]

        assert (len(docentes) == 2)

        self.se_encuentra_el_docente(self.DOCENTE_CON_NOMBRE, docentes)
        self.se_encuentra_el_docente(self.DOCENTE_SIN_NOMBRE, docentes)


if __name__ == '__main__':
    import unittest

    unittest.main()
