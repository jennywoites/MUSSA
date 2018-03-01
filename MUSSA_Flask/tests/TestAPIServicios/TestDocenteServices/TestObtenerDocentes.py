if __name__ == '__main__':
    import sys

    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase
from app import db
from app.models.horarios_models import Curso, Horario, HorarioPorCurso, CarreraPorCurso
from app.models.carreras_models import TipoMateria, Materia
from tests.TestAPIServicios.DAOMock.CarreraDAOMock import CarreraDAOMock, INGENIERIA_EN_INFORMATICA_1986
from tests.TestAPIServicios.DAOMock.DocenteDAOMock import *
import json
import datetime
from app.API_Rest.codes import *


class TestObtenerDocentes(TestBase):
    ##########################################################
    ##                   Configuracion                      ##
    ##########################################################

    FECHA = datetime.datetime.now()

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
        "carreras": [INGENIERIA_EN_INFORMATICA_1986]
    }

    def get_cursos_bd(self):
        return [self.CURSO]

    def get_test_name(self):
        return "test_obtener_docentes"

    def crear_datos_bd(self):
        carreraDAO = CarreraDAOMock()
        carreraDAO.crear_ingenieria_informatica_1986()

        self.agregar_materia()

        for horario in self.get_horarios_bd():
            self.agregar_horario(horario)

        docenteDAO = DocenteDAOMock()
        for curso in self.get_cursos_bd():
            curso_db = self.agregar_curso(curso)

            docenteDAO.crear_docente_sin_nombre()
            docenteDAO.agregar_curso_dictado(DOCENTE_SIN_NOMBRE, curso_db)

            docenteDAO.crear_docente_Woites_Jennifer()
            docenteDAO.agregar_curso_dictado(DOCENTE_WOITES_JENNIFER, curso_db)

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
            carrera_id=INGENIERIA_EN_INFORMATICA_1986["id"]
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
        return curso

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
        return (docente_servicio["id_docente"] == docente_origen[P_ID] and
                docente_servicio["apellido"] == docente_origen[P_APELLIDO] and
                docente_servicio["nombre"] == docente_origen[P_NOMBRE] and
                docente_servicio["nombre_completo"] == docente_origen[P_NOMBRE_COMPLETO] and
                self.dictan_las_mismas_materias(docente_origen, docente_servicio))

    def dictan_las_mismas_materias(self, docente_origen, docente_servicio):
        for grupo_curso_servicio in docente_servicio["materias_que_dicta"]:
            if not grupo_curso_servicio["id_curso"] in docente_origen[P_CURSOS_QUE_DICTA]:
                return False

        return len(docente_servicio["materias_que_dicta"]) == len(docente_origen[P_CURSOS_QUE_DICTA])

    ##########################################################
    ##                      Tests                           ##
    ##########################################################

    def test_obtener_los_docentes_devuelve_todos_los_docentes(self):
        client = self.app.test_client()
        response = client.get(self.get_url_obtener_todos_los_docentes())
        assert (response.status_code == SUCCESS_OK)

        docentes = json.loads(response.get_data(as_text=True))["docentes"]

        assert (len(docentes) == 2)

        self.se_encuentra_el_docente(DOCENTE_SIN_NOMBRE, docentes)
        self.se_encuentra_el_docente(DOCENTE_WOITES_JENNIFER, docentes)


if __name__ == '__main__':
    import unittest

    unittest.main()
