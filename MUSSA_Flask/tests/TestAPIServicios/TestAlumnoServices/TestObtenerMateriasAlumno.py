if __name__ == '__main__':
    import sys

    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase
from app.models.alumno_models import Alumno, MateriasAlumno, EstadoMateria
from app.models.carreras_models import Materia, TipoMateria, Carrera
from app.DAO.MateriasDAO import *
from app.API_Rest.services import *
from app.API_Rest.codes import *
import json

from datetime import datetime


class TestObtenerMateriasAlumno(TestBase):
    ##########################################################
    ##                   Configuracion                      ##
    ##########################################################

    def get_test_name(self):
        return "test_obtener_materias_alumno"

    MATERIA_PENDIENTE = {
        "estado": ESTADO_MATERIA[PENDIENTE],
        "codigo": "7514",
        "nombre": "Materia Test",
        "creditos_minimos_para_cursarla": 0,
        "creditos": 0,
        "tipo_materia_id": 1,
        "carrera": "Licenciatura en Análisis de Sistemas (1986)"
    }

    MATERIA_EN_CURSO = {
        "estado": ESTADO_MATERIA[EN_CURSO],
        "codigo": "7519",
        "nombre": "Materia Test 2",
        "creditos_minimos_para_cursarla": 0,
        "creditos": 0,
        "tipo_materia_id": 1,
        "carrera": "Licenciatura en Análisis de Sistemas (1986)"
    }

    MATERIA_FINAL_PENDIENTE = {
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

        self.crear_materia(self.MATERIA_PENDIENTE, alumno, admin_alumno, PENDIENTE, carrera)
        self.crear_materia(self.MATERIA_EN_CURSO, alumno, admin_alumno, EN_CURSO, carrera)
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
    ##              Funciones Auxiliares                    ##
    ##########################################################

    def se_encuentra_materia(self, materia, l_materias):
        for l_materia in l_materias:
            if self.son_materias_iguales(materia, l_materia):
                return True
        return False

    def son_materias_iguales(self, materia_origen, materia_servicio):
        if materia_origen["estado"] in [ESTADO_MATERIA[FINAL_PENDIENTE], ESTADO_MATERIA[APROBADA],
                                        ESTADO_MATERIA[DESAPROBADA]]:
            if not (materia_origen["aprobacion_cursada"] == materia_servicio["aprobacion_cursada"]):
                return False

        if materia_origen["estado"] in [ESTADO_MATERIA[APROBADA], ESTADO_MATERIA[DESAPROBADA]]:
            if not (materia_origen["calificacion"] == materia_servicio["calificacion"] and
                            materia_origen["acta_o_resolucion"] == materia_servicio["acta_o_resolucion"] and
                            materia_origen["forma_aprobacion_materia"] == materia_servicio[
                            "forma_aprobacion_materia"] and
                            materia_origen["fecha_aprobacion"] == materia_servicio["fecha_aprobacion"]):
                return False

        return (materia_origen["codigo"] == materia_servicio["codigo"] and
                materia_origen["nombre"] == materia_servicio["nombre"] and
                materia_origen["carrera"] == materia_servicio["carrera"])

    ##########################################################
    ##                      Tests                           ##
    ##########################################################

    def test_obtener_materias_sin_estar_logueado_da_error(self):
        client = self.app.test_client()
        response = client.get(self.get_url_get_materias_alumno())
        assert (response.status_code == REDIRECTION_FOUND)

    def test_obtener_materias_logueado_con_administrador_esta_permitido(self):
        client = self.loguear_administrador()
        response = client.get(self.get_url_get_materias_alumno())
        assert (response.status_code == SUCCESS_OK)

    def test_obtener_materias_sin_parametros_devuelve_todas_las_materias(self):
        client = self.loguear_usuario()

        response = client.get(self.get_url_get_materias_alumno())
        assert (response.status_code == SUCCESS_OK)

        materias = json.loads(response.get_data(as_text=True))["materias_alumno"]
        assert (len(materias) == 5)

    def test_obtener_materias_sin_parametros_devuelve_todas_las_materias(self):
        client = self.loguear_usuario()

        response = client.get(self.get_url_get_materias_alumno())
        assert (response.status_code == SUCCESS_OK)

        materias = json.loads(response.get_data(as_text=True))["materias_alumno"]
        assert (len(materias) == 4)

        self.se_encuentra_materia(self.MATERIA_EN_CURSO, materias)
        self.se_encuentra_materia(self.MATERIA_FINAL_PENDIENTE, materias)
        self.se_encuentra_materia(self.MATERIA_FINAL_APROBADA, materias)
        self.se_encuentra_materia(self.MATERIA_FINAL_DESAPROBADA, materias)

    def test_obtener_materias_pendientes_devuelve_solo_las_pendientes(self):
        client = self.loguear_usuario()

        response = client.get(self.get_url_get_materias_pendientes_alumno())
        assert (response.status_code == SUCCESS_OK)

        materias = json.loads(response.get_data(as_text=True))["materias_alumno"]
        assert (len(materias) == 1)

        self.se_encuentra_materia(self.MATERIA_PENDIENTE, materias)

    def test_obtener_materias_por_id_invalido_da_error(self):
        client = self.loguear_usuario()

        response = client.get(self.get_url_get_materia_alumno("5sd"))
        assert (response.status_code == CLIENT_ERROR_NOT_FOUND)

    def test_obtener_materias_por_id_inexistente_da_error(self):
        client = self.loguear_usuario()

        response = client.get(self.get_url_get_materia_alumno(56))
        assert (response.status_code == CLIENT_ERROR_NOT_FOUND)

    def test_obtener_materias_por_id_existente_perteneciente_a_otro_usuario_da_error(self):
        client = self.loguear_usuario()

        response = client.get(self.get_url_get_materia_alumno(2))
        assert (response.status_code == CLIENT_ERROR_NOT_FOUND)

    def test_obtener_materias_por_estados_devuelve_solo_materias_con_esos_estados(self):
        client = self.loguear_usuario()

        parametros = {}
        parametros["estados"] = json.dumps([APROBADA, DESAPROBADA])
        response = client.get(self.get_url_get_materias_alumno(), query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        materias = json.loads(response.get_data(as_text=True))["materias_alumno"]
        assert (len(materias) == 2)

        self.se_encuentra_materia(self.MATERIA_FINAL_DESAPROBADA, materias)
        self.se_encuentra_materia(self.MATERIA_FINAL_APROBADA, materias)

    def test_obtener_materias_por_estados_validos_pero_inexistentes_devuelve_error(self):
        client = self.loguear_usuario()

        parametros = {}
        parametros["estados"] = json.dumps([8, 9])
        response = client.get(self.get_url_get_materias_alumno(), query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_NOT_FOUND)

    def test_obtener_materias_por_estados_invalidos_devuelve_error(self):
        client = self.loguear_usuario()

        parametros = {}
        parametros["estados"] = json.dumps(["9s", 90])
        response = client.get(self.get_url_get_materias_alumno(), query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)


if __name__ == '__main__':
    import unittest

    unittest.main()
