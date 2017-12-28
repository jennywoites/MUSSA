if __name__ == '__main__':
    import sys

    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase
from app.DAO.EncuestasDAO import *
from app.DAO.MateriasDAO import *
from app.API_Rest.services import *
from app.API_Rest.codes import *
from app.models.respuestas_encuesta_models import *
from app.models.docentes_models import Docente
from app.models.horarios_models import Horario
from app.models.alumno_models import Alumno, MateriasAlumno
from app.models.palabras_clave_models import TematicaMateria, PalabraClave
from app.models.carreras_models import Carrera, Materia, TipoMateria
import json
from datetime import datetime


class TestObtenerRespuestasEncuestaAlumnoParaPreguntasEspecificas(TestBase):
    ##########################################################
    ##                   Configuracion                      ##
    ##########################################################

    def get_test_name(self):
        return "test_obtener_respuestas_encuesta_alumno_para_preguntas_especificas"

    MATERIA_FINAL_DESAPROBADA = {
        "id": 1,
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
        "carrera": "9 - Licenciatura",
        "materia": "6122 - Una materia",
        "curso": "25: Apellido-Apellido2",
        "cuatrimestre_aprobacion_cursada": "1",
        "anio_aprobacion_cursada": "2017",
        "fecha_aprobacion": "1C / 2017",
        "finalizada": False
    }

    def crear_datos_bd(self):
        create_encuestas()

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

        self.crear_materia(self.MATERIA_FINAL_DESAPROBADA, alumno, admin_alumno, DESAPROBADA, carrera)

        encuesta = EncuestaAlumno(
            alumno_id=self.ENCUESTA["alumno_id"],
            materia_alumno_id=self.ENCUESTA["materia_alumno_id"],
            carrera=self.ENCUESTA["carrera"],
            materia=self.ENCUESTA["materia"],
            curso=self.ENCUESTA["curso"],
            cuatrimestre_aprobacion_cursada=self.ENCUESTA["cuatrimestre_aprobacion_cursada"],
            anio_aprobacion_cursada=self.ENCUESTA["anio_aprobacion_cursada"],
            finalizada=self.ENCUESTA["finalizada"]
        )
        db.session.add(encuesta)
        db.session.commit()

    def crear_materia(self, materia_dict, alumno, admin, v_estado, carrera):
        estado = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[v_estado]).first()

        materia = self.crear_materia_con_carrera(materia_dict, carrera)

        self.agregar_materia_alumno(alumno, materia_dict, materia, carrera, estado)
        self.agregar_materia_alumno(admin, materia_dict, materia, carrera, estado)

    def crear_materia_con_carrera(self, materia_dict, carrera):
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

        return materia

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

    def crear_respuestas_alumno(self, encuesta, preguntas):
        for pregunta in preguntas:
            tipo_encuesta = TipoEncuesta.query.filter_by(tipo=pregunta["tipo_num"]).first()

            respuesta_encuesta = RespuestaEncuestaAlumno(
                encuesta_alumno_id=encuesta.id,
                pregunta_encuesta_id=pregunta["pregunta_encuesta_id"],
                tipo_id=tipo_encuesta.id
            )
            db.session.add(respuesta_encuesta)
            db.session.commit()

            self.crear_respuesta_automatica(respuesta_encuesta, tipo_encuesta.tipo)
            db.session.commit()

    def crear_respuesta_automatica(self, respuesta_encuesta, tipo_encuesta):
        if tipo_encuesta == PUNTAJE_1_A_5:
            return self.generar_respuesta_puntaje(respuesta_encuesta)

        if tipo_encuesta == TEXTO_LIBRE:
            return self.generar_respuesta_texto_libre(respuesta_encuesta)

        if tipo_encuesta == SI_NO:
            return self.generar_respuesta_si_no(respuesta_encuesta)

        if tipo_encuesta == HORARIO:
            return self.generar_respuesta_horario(respuesta_encuesta)

        if tipo_encuesta == DOCENTE:
            return self.generar_respuesta_docente(respuesta_encuesta)

        if tipo_encuesta == CORRELATIVA:
            return self.generar_respuesta_correlativas(respuesta_encuesta)

        if tipo_encuesta == ESTRELLAS:
            return self.generar_respuesta_estrellas(respuesta_encuesta)

        if tipo_encuesta == NUMERO:
            return self.generar_respuesta_numero(respuesta_encuesta)

        if tipo_encuesta == TAG:
            return self.generar_respuesta_tags(respuesta_encuesta)

        # if tipo_encuesta == TEMATICA:
        return self.generar_respuesta_tematicas(respuesta_encuesta)

    RESPUESTA_PUNTAJE = 5

    def generar_respuesta_puntaje(self, respuesta_encuesta):
        db.session.add(RespuestaEncuestaPuntaje(
            rta_encuesta_alumno_id=respuesta_encuesta.id,
            puntaje=self.RESPUESTA_PUNTAJE
        ))

    RESPUESTA_TEXTO_LIBRE = "Este es un texto libre de hasta 250 caracteres"

    def generar_respuesta_texto_libre(self, respuesta_encuesta):
        db.session.add(RespuestaEncuestaTexto(
            rta_encuesta_alumno_id=respuesta_encuesta.id,
            texto=self.RESPUESTA_TEXTO_LIBRE
        ))

    RESPUESTA_SI_NO = False

    def generar_respuesta_si_no(self, respuesta_encuesta):
        db.session.add(RespuestaEncuestaSiNo(
            rta_encuesta_alumno_id=respuesta_encuesta.id,
            respuesta=self.RESPUESTA_SI_NO
        ))

    RESPUESTA_HORARIOS = [
        {
            "dia": "Lunes",
            "hora_desde": "7.5",
            "hora_hasta": "11",
            "hora_desde_reloj": "07:30",
            "hora_hasta_reloj": "11:00"
        },
        {
            "dia": "Martes",
            "hora_desde": "12",
            "hora_hasta": "15",
            "hora_desde_reloj": "12:00",
            "hora_hasta_reloj": "15:00"
        }
    ]

    def generar_respuesta_horario(self, respuesta_encuesta):
        for datos_horario in self.RESPUESTA_HORARIOS:
            horario = Horario(
                dia=datos_horario["dia"],
                hora_desde=datos_horario["hora_desde"],
                hora_hasta=datos_horario["hora_hasta"]
            )
            db.session.add(horario)
            db.session.commit()

            db.session.add(RespuestaEncuestaHorario(
                rta_encuesta_alumno_id=respuesta_encuesta.id,
                horario_id=horario.id
            ))

    RESPUESTA_DOCENTE = {
        "apellido": "Wainer",
        "nombre": "Ariel",
        "nombre_completo": "Wainer, Ariel",
        "comentario": "Este es un comentario de hasta 250 caracteres para un docente"
    }

    def generar_respuesta_docente(self, respuesta_encuesta):
        docente = Docente(
            apellido=self.RESPUESTA_DOCENTE["apellido"],
            nombre=self.RESPUESTA_DOCENTE["nombre"]
        )
        db.session.add(docente)
        db.session.commit()

        db.session.add(RespuestaEncuestaDocente(
            rta_encuesta_alumno_id=respuesta_encuesta.id,
            docente_id=docente.id,
            comentario=self.RESPUESTA_DOCENTE["comentario"]
        ))

    RESPUESTA_CORRELATIVAS = [
        {
            "codigo": "1234",
            "nombre": "Materia Test 1",
            "creditos_minimos_para_cursarla": 5,
            "creditos": 8,
            "tipo_materia_id": 1,
        },
        {
            "codigo": "9875",
            "nombre": "Materia Test 2",
            "creditos_minimos_para_cursarla": 0,
            "creditos": 12,
            "tipo_materia_id": 1,
        }
    ]

    def generar_respuesta_correlativas(self, respuesta_encuesta):
        carrera = Carrera.query.first()
        for datos_correlativa in self.RESPUESTA_CORRELATIVAS:
            materia = self.crear_materia_con_carrera(datos_correlativa, carrera)

            db.session.add(RespuestaEncuestaCorrelativa(
                rta_encuesta_alumno_id=respuesta_encuesta.id,
                materia_correlativa_id=materia.id
            ))

    RESPUESTA_ESTRELLAS = 5

    def generar_respuesta_estrellas(self, respuesta_encuesta):
        db.session.add(RespuestaEncuestaEstrellas(
            rta_encuesta_alumno_id=respuesta_encuesta.id,
            estrellas=self.RESPUESTA_ESTRELLAS
        ))

    RESPUESTA_NUMERO = 3

    def generar_respuesta_numero(self, respuesta_encuesta):
        db.session.add(RespuestaEncuestaNumero(
            rta_encuesta_alumno_id=respuesta_encuesta.id,
            numero=self.RESPUESTA_NUMERO
        ))

    RESPUESTAS_PALABRAS_CLAVE = [
        "Palabra clave 1",
        "Palabra clave 2",
        "Palabra clave 3"
    ]

    def generar_respuesta_tags(self, respuesta_encuesta):
        for palabra_clave in self.RESPUESTAS_PALABRAS_CLAVE:
            palabra = PalabraClave(palabra=palabra_clave)
            db.session.add(palabra)
            db.session.commit()

            db.session.add(RespuestaEncuestaTags(
                rta_encuesta_alumno_id=respuesta_encuesta.id,
                palabra_clave_id=palabra.id
            ))

    RESPUESTAS_TEMATICAS = [
        "Tematica 1",
        "Tematica 2"
    ]

    def generar_respuesta_tematicas(self, respuesta_encuesta):
        for tema in self.RESPUESTAS_TEMATICAS:
            tematica = TematicaMateria(tematica=tema)
            db.session.add(tematica)
            db.session.commit()

            db.session.add(RespuestaEncuestaTematica(
                rta_encuesta_alumno_id=respuesta_encuesta.id,
                tematica_id=tematica.id
            ))

    ##########################################################
    ##                      Tests                           ##
    ##########################################################

    def test_obtener_respuestas_sin_estar_logueado_redirecciona_al_loguin(self):
        client = self.app.test_client()
        response = client.get(OBTENER_RESPUESTAS_ALUMNO_PARA_PREGUNTAS_ESPECIFICAS_SERVICE)
        assert (response.status_code == REDIRECTION_FOUND)

    def test_obtener_las_respuestas_de_preguntas_no_contestadas_devuelve_lista_vacia(self):
        client = self.loguear_usuario()

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        response = client.get(OBTENER_RESPUESTAS_ALUMNO_PARA_PREGUNTAS_ESPECIFICAS_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas_encuestas = json.loads(response.get_data(as_text=True))["respuestas_encuestas"]
        assert (len(respuestas_encuestas) == 0)

    def test_obtener_las_respuestas_de_una_encuesta_que_no_le_pertenece_da_error(self):
        client = self.loguear_administrador()

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        response = client.get(OBTENER_RESPUESTAS_ALUMNO_PARA_PREGUNTAS_ESPECIFICAS_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_obtener_las_respuestas_con_id_encuesta_inexistente_da_error(self):
        client = self.loguear_administrador()

        parametros = {}
        parametros["id_encuesta"] = 5
        response = client.get(OBTENER_RESPUESTAS_ALUMNO_PARA_PREGUNTAS_ESPECIFICAS_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_obtener_las_respuestas_con_id_encuesta_invalido_da_error(self):
        client = self.loguear_administrador()

        parametros = {}
        parametros["id_encuesta"] = "pepe"
        response = client.get(OBTENER_RESPUESTAS_ALUMNO_PARA_PREGUNTAS_ESPECIFICAS_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_obtener_las_respuestas_de_todas_las_preguntas_con_respuestas_las_obtiene_a_todas(self):
        client = self.loguear_usuario()

        encuesta = EncuestaAlumno.query.first()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE)
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]

        self.crear_respuestas_alumno(encuesta, preguntas)

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        response = client.get(OBTENER_RESPUESTAS_ALUMNO_PARA_PREGUNTAS_ESPECIFICAS_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas_encuestas = json.loads(response.get_data(as_text=True))["respuestas_encuestas"]
        assert (len(respuestas_encuestas) == 32)

    def test_obtener_las_respuestas_de_preguntas_especificas_solo_obtiene_esas(self):
        client = self.loguear_usuario()

        encuesta = EncuestaAlumno.query.first()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE)
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]

        self.crear_respuestas_alumno(encuesta, preguntas)

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["ids_preguntas"] = "3;8;7;11"
        response = client.get(OBTENER_RESPUESTAS_ALUMNO_PARA_PREGUNTAS_ESPECIFICAS_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas_encuestas = json.loads(response.get_data(as_text=True))["respuestas_encuestas"]
        assert (len(respuestas_encuestas) == 4)

        assert (respuestas_encuestas['3']["texto"] == self.RESPUESTA_TEXTO_LIBRE)

        for tema_guardado in self.RESPUESTAS_TEMATICAS:
            encontrado = False
            for tema in respuestas_encuestas['7']["tematicas"]:
                if tema["tematica"] == tema_guardado:
                    encontrado = True
            assert (encontrado)

        for horario_guardado in self.RESPUESTA_HORARIOS:
            encontrado = False
            for horario in respuestas_encuestas['8']["horarios"]:
                if (horario["dia"] == horario_guardado["dia"] and
                        horario["hora_desde"] == horario_guardado["hora_desde"] and
                        horario["hora_hasta"] == horario_guardado["hora_hasta"]):
                    encontrado = True
            assert (encontrado)

        assert (respuestas_encuestas['11']["puntaje"] == self.RESPUESTA_PUNTAJE)

    def test_obtener_las_respuestas_con_lista_vacia_de_preguntas_devuelve_todas(self):
        client = self.loguear_usuario()

        encuesta = EncuestaAlumno.query.first()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE)
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]

        self.crear_respuestas_alumno(encuesta, preguntas)

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["ids_preguntas"] = ""
        response = client.get(OBTENER_RESPUESTAS_ALUMNO_PARA_PREGUNTAS_ESPECIFICAS_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas_encuestas = json.loads(response.get_data(as_text=True))["respuestas_encuestas"]
        assert (len(respuestas_encuestas) == 32)

    def test_obtener_las_respuestas_con_ids_de_preguntas_inexistentes_da_error(self):
        client = self.loguear_administrador()

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["ids_preguntas"] = "41;59"
        response = client.get(OBTENER_RESPUESTAS_ALUMNO_PARA_PREGUNTAS_ESPECIFICAS_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_obtener_las_respuestas_con_ids_de_preguntas_existentes_separador_invalido_da_error(self):
        client = self.loguear_administrador()

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["ids_preguntas"] = "2-3-9"
        response = client.get(OBTENER_RESPUESTAS_ALUMNO_PARA_PREGUNTAS_ESPECIFICAS_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_obtener_las_respuestas_con_ids_de_preguntas_invalidos_da_error(self):
        client = self.loguear_administrador()

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["ids_preguntas"] = "5;pepe;3;!2"
        response = client.get(OBTENER_RESPUESTAS_ALUMNO_PARA_PREGUNTAS_ESPECIFICAS_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)


if __name__ == '__main__':
    import unittest

    unittest.main()
