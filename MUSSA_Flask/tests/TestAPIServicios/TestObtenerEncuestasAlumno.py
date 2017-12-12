if __name__ == '__main__':
    import sys

    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase
from app.API_Rest.services import *
from app.API_Rest.codes import *
from app.DAO.MateriasDAO import *
from app.models.respuestas_encuesta_models import EncuestaAlumno
from app.models.alumno_models import Alumno, MateriasAlumno
from app.models.carreras_models import Carrera, Materia, TipoMateria
import json
from datetime import datetime


class TestObtenerEncuestasAlumno(TestBase):
    ##########################################################
    ##                   Configuracion                      ##
    ##########################################################

    def get_test_name(self):
        return "test_obtener_encuestas_alumno"

    MATERIA_FINAL_PENDIENTE = {
        "id": 1,
        "estado": ESTADO_MATERIA[FINAL_PENDIENTE],
        "codigo": "1572",
        "nombre": "Materia Test 3",
        "creditos_minimos_para_cursarla": 0,
        "creditos": 0,
        "tipo_materia_id": 1,
        "carrera": "Licenciatura en Análisis de Sistemas (1986)",
        "cuatrimestre_aprobacion_cursada": "1",
        "anio_aprobacion_cursada": "2016",
        'aprobacion_cursada': "1C / 2016",
    }

    MATERIA_FINAL_APROBADA = {
        "id": 2,
        "estado": ESTADO_MATERIA[APROBADA],
        "codigo": "1572",
        "nombre": "Materia Test 3",
        "creditos_minimos_para_cursarla": 0,
        "creditos": 0,
        "tipo_materia_id": 1,
        "carrera": "Licenciatura en Análisis de Sistemas (1986)",
        "cuatrimestre_aprobacion_cursada": "2",
        "anio_aprobacion_cursada": "2017",
        'aprobacion_cursada': "2C / 2017",
        "calificacion": 7,
        "fecha_aprobacion": datetime.now(),
        "acta_o_resolucion": "5555-899",
        "forma_aprobacion_id": 1,
        "forma_aprobacion_materia": "Examen"
    }

    MATERIA_FINAL_DESAPROBADA = {
        "id": 3,
        "estado": ESTADO_MATERIA[DESAPROBADA],
        "codigo": "1572",
        "nombre": "Materia Test 3",
        "creditos_minimos_para_cursarla": 0,
        "creditos": 0,
        "tipo_materia_id": 1,
        "carrera": "Licenciatura en Análisis de Sistemas (1986)",
        "cuatrimestre_aprobacion_cursada": "2",
        "anio_aprobacion_cursada": "2017",
        'aprobacion_cursada': "2C / 2017",
        "calificacion": 7,
        "fecha_aprobacion": datetime.now(),
        "acta_o_resolucion": "5555-899",
        "forma_aprobacion_id": 1,
        "forma_aprobacion_materia": "Examen"
    }

    ENCUESTA = {
        "alumno_id": 1,
        "materia_alumno_id": MATERIA_FINAL_DESAPROBADA["id"],
        "carrera": "Una carrera",
        "materia": "Una materia",
        "curso": "Un curso",
        "cuatrimestre_aprobacion_cursada": "1",
        "anio_aprobacion_cursada": "2017",
        "fecha_aprobacion": "1C / 2017",
        "finalizada": False
    }

    def crear_datos_bd(self):
        carrera = Carrera(
            codigo='9',
            nombre='Licenciatura en Análisis de Sistemas',
            duracion_estimada_en_cuatrimestres=9,
            requiere_prueba_suficiencia_de_idioma=False,
            plan="1986"
        )
        db.session.add(carrera)

        tipo_materia = TipoMateria(descripcion="Tipo Materia Test")
        db.session.add(tipo_materia)
        db.session.commit()

        alumno = Alumno(user_id=self.get_usuario().id)
        db.session.add(alumno)
        db.session.commit()

        admin_alumno = Alumno(user_id=self.get_administrador().id)
        db.session.add(admin_alumno)
        db.session.commit()

        self.crear_materia(self.MATERIA_FINAL_PENDIENTE, alumno, admin_alumno, FINAL_PENDIENTE, carrera)
        self.crear_materia(self.MATERIA_FINAL_APROBADA, alumno, admin_alumno, APROBADA, carrera)
        self.crear_materia(self.MATERIA_FINAL_DESAPROBADA, alumno, admin_alumno, DESAPROBADA, carrera)

    def crear_materia(self, materia_dict, alumno, admin, v_estado, carrera):
        estado = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[v_estado]).first()

        materia = Materia(
            codigo=materia_dict["codigo"],
            nombre=materia_dict["nombre"],
            creditos_minimos_para_cursarla=materia_dict["creditos_minimos_para_cursarla"],
            creditos=materia_dict["creditos"],
            tipo_materia_id=materia_dict["tipo_materia_id"],
            carrera_id=carrera.id,
        )
        db.session.add(materia)
        db.session.commit()

        self.agregar_materia_alumno(alumno, materia_dict, materia, carrera, estado)
        self.agregar_materia_alumno(admin, materia_dict, materia, carrera, estado)

    def agregar_materia_alumno(self, alumno, materia_dict, materia, carrera, estado):
        materia_alumno = MateriasAlumno(
            alumno_id=alumno.id,
            materia_id=materia.id,
            carrera_id=carrera.id,
            estado_id=estado.id,
        )

        if "calificacion" in materia_dict:
            materia_alumno.calificacion = materia_dict["calificacion"]

        if "fecha_aprobacion" in materia_dict:
            materia_alumno.fecha_aprobacion = materia_dict["fecha_aprobacion"]

        if "cuatrimestre_aprobacion_cursada" in materia_dict:
            materia_alumno.cuatrimestre_aprobacion_cursada = materia_dict["cuatrimestre_aprobacion_cursada"]

        if "anio_aprobacion_cursada" in materia_dict:
            materia_alumno.anio_aprobacion_cursada = materia_dict["anio_aprobacion_cursada"]

        if "acta_o_resolucion" in materia_dict:
            materia_alumno.acta_o_resolucion = materia_dict["acta_o_resolucion"]

        if "forma_aprobacion_id" in materia_dict:
            materia_alumno.forma_aprobacion_id = materia_dict["forma_aprobacion_id"]

        db.session.add(materia_alumno)

    ##########################################################
    ##                      Tests                           ##
    ##########################################################

    def test_obtener_encuestas_sin_estar_logueado_da_error(self):
        client = self.app.test_client()
        response = client.get(OBTENER_ENCUESTAS_ALUMNO_SERVICE)
        assert (response.status_code == REDIRECTION_FOUND)

    def test_obtener_encuestas_logueado_con_administrador_esta_permitido(self):
        client = self.loguear_administrador()
        response = client.get(OBTENER_ENCUESTAS_ALUMNO_SERVICE)
        assert (response.status_code == SUCCESS_OK)

    def test_obtener_encuestas_alumno_sin_encuestas(self):
        client = self.loguear_usuario()

        response = client.get(OBTENER_ENCUESTAS_ALUMNO_SERVICE)
        assert (response.status_code == SUCCESS_OK)

        encuestas = json.loads(response.get_data(as_text=True))["encuestas"]
        assert (len(encuestas) == 0)

    def test_obtener_encuestas_alumno_sin_encuestas(self):
        db.session.add(EncuestaAlumno(
            alumno_id=self.ENCUESTA["alumno_id"],
            materia_alumno_id=self.ENCUESTA["materia_alumno_id"],
            carrera=self.ENCUESTA["carrera"],
            materia=self.ENCUESTA["materia"],
            curso=self.ENCUESTA["curso"],
            cuatrimestre_aprobacion_cursada=self.ENCUESTA["cuatrimestre_aprobacion_cursada"],
            anio_aprobacion_cursada=self.ENCUESTA["anio_aprobacion_cursada"],
            finalizada=self.ENCUESTA["finalizada"]
        ))
        db.session.commit()

        client = self.loguear_usuario()

        response = client.get(OBTENER_ENCUESTAS_ALUMNO_SERVICE)
        assert (response.status_code == SUCCESS_OK)

        encuestas = json.loads(response.get_data(as_text=True))["encuestas"]
        assert (len(encuestas) == 1)


if __name__ == '__main__':
    import unittest

    unittest.main()
