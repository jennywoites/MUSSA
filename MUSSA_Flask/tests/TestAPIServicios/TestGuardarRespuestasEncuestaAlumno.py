if __name__ == '__main__':
    import sys

    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase
from app.DAO.MateriasDAO import *
from app.API_Rest.services import *
from app.API_Rest.codes import *
from app.models.respuestas_encuesta_models import *
from app.models.alumno_models import Alumno, MateriasAlumno
from app.models.carreras_models import Carrera, Materia, TipoMateria
from app.models.docentes_models import Docente
import json
from datetime import datetime


class TestGuardarRespuestasEncuestaAlumno(TestBase):
    ##########################################################
    ##                   Configuracion                      ##
    ##########################################################

    def get_test_name(self):
        return "test_guardar_respuestas_encuesta_alumno"

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

    MATERIA_DEFAULT_CORRELATIVA = {
        "id": 2,
        "codigo": "5896",
        "nombre": "Materia Default Correlativa",
        "creditos_minimos_para_cursarla": 0,
        "creditos": 10,
        "tipo_materia_id": 1,
    }

    MATERIA_NO_CORRELATIVA = {
        "id": 3,
        "codigo": "1987",
        "nombre": "Materia No Correlativa",
        "creditos_minimos_para_cursarla": 3,
        "creditos": 8,
        "tipo_materia_id": 1,
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

    DOCENTE_1 = {
        "apellido": "Wainer",
        "nombre": "Ariel"
    }

    DOCENTE_2 = {
        "apellido": "Essaya",
        "nombre": "Diego"
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

        self.inicializar_encuesta_alumno()

        self.crear_materia_con_carrera(self.MATERIA_DEFAULT_CORRELATIVA, carrera)
        self.crear_materia_con_carrera(self.MATERIA_NO_CORRELATIVA, carrera)

        for docente in [self.DOCENTE_1, self.DOCENTE_2]:
            self.crear_docente(docente)

    def inicializar_encuesta_alumno(self):
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

        estado_pasos = EstadoPasosEncuestaAlumno(encuesta_alumno_id=encuesta.id)
        estado_pasos.inicializar_pasos()
        db.session.add(estado_pasos)
        db.session.commit()

    def crear_docente(self, docente):
        db.session.add(Docente(
            apellido=docente["apellido"],
            nombre=docente["nombre"]
        ))
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

    def crear_respuestas_alumno(self, preguntas, datos_respuestas):
        respuestas_preguntas = []
        for pregunta in preguntas:
            tipo_encuesta = TipoEncuesta.query.filter_by(tipo=pregunta["tipo_num"]).first()
            id_pregunta = pregunta["pregunta_encuesta_id"]
            respuesta_automatica = self.crear_respuesta_automatica(id_pregunta, tipo_encuesta.tipo, datos_respuestas)
            if respuesta_automatica:
                respuestas_preguntas.append(respuesta_automatica)
        return json.dumps(respuestas_preguntas)

    def crear_respuesta_automatica(self, id_pregunta, tipo_encuesta, datos_respuestas):
        acciones = {
            PUNTAJE_1_A_5: self.generar_respuesta_puntaje,
            TEXTO_LIBRE: self.generar_respuesta_texto_libre,
            SI_NO: self.generar_respuesta_si_no,
            HORARIO: self.generar_respuesta_horario,
            DOCENTE: self.generar_respuesta_docente,
            CORRELATIVA: self.generar_respuesta_correlativas,
            ESTRELLAS: self.generar_respuesta_estrellas,
            NUMERO: self.generar_respuesta_numero,
            TAG: self.generar_respuesta_tags,
            TEMATICA: self.generar_respuesta_tematicas,
        }

        if tipo_encuesta in datos_respuestas:
            return acciones[tipo_encuesta](id_pregunta, datos_respuestas[tipo_encuesta])

        return None

    def generar_respuesta_puntaje(self, id_pregunta, datos_respuesta):
        return {
            "idPregunta": id_pregunta,
            "tipo_encuesta": PUNTAJE_1_A_5,
            "puntaje": datos_respuesta["puntaje"]
        }

    def generar_respuesta_texto_libre(self, id_pregunta, datos_respuesta):
        return {
            "idPregunta": id_pregunta,
            "tipo_encuesta": TEXTO_LIBRE,
            "texto": datos_respuesta["texto"]
        }

    def generar_respuesta_si_no(self, id_pregunta, datos_respuesta):
        return {
            "idPregunta": id_pregunta,
            "tipo_encuesta": SI_NO,
            "respuesta": datos_respuesta["respuesta"]
        }

    def generar_respuesta_horario(self, id_pregunta, datos_respuesta):
        horarios = []
        for datos_horario in datos_respuesta["horarios"]:
            horarios.append({
                "dia": datos_horario["dia"],
                "hora_desde": datos_horario["hora_desde_reloj"],
                "hora_hasta": datos_horario["hora_hasta_reloj"]
            })

        return {
            "idPregunta": id_pregunta,
            "tipo_encuesta": HORARIO,
            "horarios": horarios
        }

    def generar_respuesta_docente(self, id_pregunta, datos_respuesta):
        respuestas_docentes = []
        for docente in datos_respuesta["docentes"]:
            respuestas_docentes.append({
                "id_docente": docente["id_docente"],
                "comentario": docente["comentario"]
            })

        return {
            "idPregunta": id_pregunta,
            "tipo_encuesta": DOCENTE,
            "docentes": respuestas_docentes
        }

    def generar_respuesta_correlativas(self, id_pregunta, datos_respuesta):
        return {
            "idPregunta": id_pregunta,
            "tipo_encuesta": CORRELATIVA,
            "correlativas": datos_respuesta["correlativas"]
        }

    def generar_respuesta_estrellas(self, id_pregunta, datos_respuesta):
        return {
            "idPregunta": id_pregunta,
            "tipo_encuesta": ESTRELLAS,
            "estrellas": datos_respuesta["estrellas"]
        }

    def generar_respuesta_numero(self, id_pregunta, datos_respuesta):
        return {
            "idPregunta": id_pregunta,
            "tipo_encuesta": NUMERO,
            "numero": datos_respuesta["numero"]
        }

    def generar_respuesta_tags(self, id_pregunta, datos_respuesta):
        return {
            "idPregunta": id_pregunta,
            "tipo_encuesta": TAG,
            "palabras_clave": datos_respuesta["palabras_clave"]
        }

    def generar_respuesta_tematicas(self, id_pregunta, datos_respuesta):
        return {
            "idPregunta": id_pregunta,
            "tipo_encuesta": TEMATICA,
            "tematicas": datos_respuesta["tematicas"]
        }

    def get_datos_respuestas_default(self):
        return {
            PUNTAJE_1_A_5: {
                "puntaje": 5
            },
            TEXTO_LIBRE: {
                "texto": "Este es un texto libre de hasta 250 caracteres"
            },
            SI_NO: {
                "respuesta": False
            },
            HORARIO: {
                "horarios": [
                    {
                        "dia": "Lunes",
                        "hora_desde": "7.5",
                        "hora_desde_reloj": "07:30",
                        "hora_hasta": "11",
                        "hora_hasta_reloj": "11:00"
                    },
                    {
                        "dia": "Martes",
                        "hora_desde": "12",
                        "hora_desde_reloj": "12:00",
                        "hora_hasta": "15",
                        "hora_hasta_reloj": "15:00"
                    }
                ]
            },
            DOCENTE: {
                "docentes": [
                    {
                        "id_docente": 1,
                        "comentario": "Este es un comentario de hasta 250 caracteres para un docente"
                    }
                ]
            },
            CORRELATIVA: {
                "correlativas": [
                    self.MATERIA_DEFAULT_CORRELATIVA["id"]
                ]
            },
            ESTRELLAS: {
                "estrellas": 5
            },
            NUMERO: {
                "numero": 3
            },
            TAG: {
                "palabras_clave": [
                    "Palabra clave 1",
                    "Palabra clave 2",
                    "Palabra clave 3"
                ]
            },
            TEMATICA: {
                "tematicas": [
                    "Tematica 1",
                    "Tematica 2"
                ]
            },
        }

    def obtener_respuestas_guardadas_alumno(self, preguntas, encuesta, client):
        ids_preguntas = ""
        for pregunta in preguntas:
            ids_preguntas += str(pregunta["pregunta_encuesta_id"]) + ";"

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["ids_preguntas"] = ids_preguntas[:-1]
        response = client.get(OBTENER_RESPUESTAS_ALUMNO_PARA_PREGUNTAS_ESPECIFICAS_SERVICE, query_string=parametros)
        return json.loads(response.get_data(as_text=True))["respuestas_encuestas"]

    ##########################################################
    ##                      Tests                           ##
    ##########################################################

    def test_guardar_respuestas_sin_estar_logueado_redirecciona_al_loguin(self):
        client = self.app.test_client()
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE)
        assert (response.status_code == REDIRECTION_FOUND)

    def test_guardar_respuestas_encuestas_en_blanco_categoria_general_las_guarda_correctamente(self):
        paso_actual = GRUPO_ENCUESTA_GENERAL

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, self.get_datos_respuestas_default())
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert (len(preguntas) == len(respuestas))

    def test_guardar_respuestas_encuestas_en_blanco_categoria_contenido_las_guarda_correctamente(self):
        paso_actual = GRUPO_ENCUESTA_CONTENIDO

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, self.get_datos_respuestas_default())
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert (len(preguntas) == len(respuestas))

    def test_guardar_respuestas_encuestas_en_blanco_categoria_clases_las_guarda_correctamente(self):
        paso_actual = GRUPO_ENCUESTA_CLASES

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, self.get_datos_respuestas_default())
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert (len(preguntas) == len(respuestas))

    def test_guardar_respuestas_encuestas_en_blanco_categoria_examenes_las_guarda_correctamente(self):
        paso_actual = GRUPO_ENCUESTA_EXAMENES

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, self.get_datos_respuestas_default())
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert (len(preguntas) == len(respuestas))

    def test_guardar_respuestas_encuestas_en_blanco_categoria_docentes_las_guarda_correctamente(self):
        paso_actual = GRUPO_ENCUESTA_DOCENTES

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, self.get_datos_respuestas_default())
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert (len(preguntas) == len(respuestas))

    def test_guardar_respuestas_parciales_en_categoria_general_guarda_correctamente(self):
        paso_actual = GRUPO_ENCUESTA_GENERAL

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[0], preguntas[3],preguntas[8],preguntas[10], preguntas[12], preguntas[13]]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, self.get_datos_respuestas_default())
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert (len(preguntas) == len(respuestas))

    def test_guardar_respuestas_de_una_categoria_en_otra_incorrecta_da_error(self):
        paso_actual = GRUPO_ENCUESTA_GENERAL

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[0], preguntas[3],preguntas[8],preguntas[10], preguntas[12], preguntas[13]]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = GRUPO_ENCUESTA_EXAMENES
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, self.get_datos_respuestas_default())
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_guardar_respuestas_completas_en_categoria_contenido_guarda_correctamente_y_el_paso_queda_finalizado(self):
        paso_actual = GRUPO_ENCUESTA_CONTENIDO

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]

        encuesta = EncuestaAlumno.query.first()

        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).first()

        assert(estados_pasos.estadoPaso1 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_GENERAL
        assert(estados_pasos.estadoPaso2 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CONTENIDO
        assert(estados_pasos.estadoPaso3 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CLASES
        assert(estados_pasos.estadoPaso4 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_EXAMENES
        assert(estados_pasos.estadoPaso5 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_DOCENTES

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, self.get_datos_respuestas_default())
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert (len(preguntas) == len(respuestas))

        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).first()

        assert(estados_pasos.estadoPaso1 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_GENERAL
        assert(estados_pasos.estadoPaso2 == PASO_ENCUESTA_FINALIZADO) #GRUPO_ENCUESTA_CONTENIDO
        assert(estados_pasos.estadoPaso3 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CLASES
        assert(estados_pasos.estadoPaso4 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_EXAMENES
        assert(estados_pasos.estadoPaso5 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_DOCENTES

    def test_guardar_respuestas_parciales_en_categoria_contenido_guarda_correctamente_y_el_paso_queda_en_curso(self):
        paso_actual = GRUPO_ENCUESTA_CONTENIDO

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[0], preguntas[3],preguntas[6]]

        encuesta = EncuestaAlumno.query.first()

        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).first()

        assert(estados_pasos.estadoPaso1 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_GENERAL
        assert(estados_pasos.estadoPaso2 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CONTENIDO
        assert(estados_pasos.estadoPaso3 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CLASES
        assert(estados_pasos.estadoPaso4 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_EXAMENES
        assert(estados_pasos.estadoPaso5 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_DOCENTES

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, self.get_datos_respuestas_default())
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert (len(preguntas) == len(respuestas))

        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).first()

        assert(estados_pasos.estadoPaso1 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_GENERAL
        assert(estados_pasos.estadoPaso2 == PASO_ENCUESTA_EN_CURSO) #GRUPO_ENCUESTA_CONTENIDO
        assert(estados_pasos.estadoPaso3 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CLASES
        assert(estados_pasos.estadoPaso4 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_EXAMENES
        assert(estados_pasos.estadoPaso5 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_DOCENTES

    def test_guardar_nuevas_respuestas_parciales_sobre_paso_finalizado_queda_en_curso(self):
        paso_actual = GRUPO_ENCUESTA_CONTENIDO

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]

        encuesta = EncuestaAlumno.query.first()

        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).first()

        assert(estados_pasos.estadoPaso1 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_GENERAL
        assert(estados_pasos.estadoPaso2 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CONTENIDO
        assert(estados_pasos.estadoPaso3 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CLASES
        assert(estados_pasos.estadoPaso4 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_EXAMENES
        assert(estados_pasos.estadoPaso5 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_DOCENTES

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, self.get_datos_respuestas_default())
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert (len(preguntas) == len(respuestas))

        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).first()

        assert(estados_pasos.estadoPaso1 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_GENERAL
        assert(estados_pasos.estadoPaso2 == PASO_ENCUESTA_FINALIZADO) #GRUPO_ENCUESTA_CONTENIDO
        assert(estados_pasos.estadoPaso3 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CLASES
        assert(estados_pasos.estadoPaso4 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_EXAMENES
        assert(estados_pasos.estadoPaso5 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_DOCENTES

        preguntas = [preguntas[0], preguntas[3],preguntas[6]]
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, self.get_datos_respuestas_default())
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert (len(preguntas) == len(respuestas))

        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).first()

        assert(estados_pasos.estadoPaso1 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_GENERAL
        assert(estados_pasos.estadoPaso2 == PASO_ENCUESTA_EN_CURSO) #GRUPO_ENCUESTA_CONTENIDO
        assert(estados_pasos.estadoPaso3 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CLASES
        assert(estados_pasos.estadoPaso4 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_EXAMENES
        assert(estados_pasos.estadoPaso5 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_DOCENTES

    def test_guardar_nuevas_respuestas_completas_sobre_paso_finalizado_queda_finalizado(self):
        paso_actual = GRUPO_ENCUESTA_CONTENIDO

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]

        encuesta = EncuestaAlumno.query.first()

        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).first()

        assert(estados_pasos.estadoPaso1 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_GENERAL
        assert(estados_pasos.estadoPaso2 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CONTENIDO
        assert(estados_pasos.estadoPaso3 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CLASES
        assert(estados_pasos.estadoPaso4 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_EXAMENES
        assert(estados_pasos.estadoPaso5 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_DOCENTES

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, self.get_datos_respuestas_default())
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert (len(preguntas) == len(respuestas))

        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).first()

        assert(estados_pasos.estadoPaso1 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_GENERAL
        assert(estados_pasos.estadoPaso2 == PASO_ENCUESTA_FINALIZADO) #GRUPO_ENCUESTA_CONTENIDO
        assert(estados_pasos.estadoPaso3 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CLASES
        assert(estados_pasos.estadoPaso4 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_EXAMENES
        assert(estados_pasos.estadoPaso5 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_DOCENTES

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, self.get_datos_respuestas_default())
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert (len(preguntas) == len(respuestas))

        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).first()

        assert(estados_pasos.estadoPaso1 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_GENERAL
        assert(estados_pasos.estadoPaso2 == PASO_ENCUESTA_FINALIZADO) #GRUPO_ENCUESTA_CONTENIDO
        assert(estados_pasos.estadoPaso3 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CLASES
        assert(estados_pasos.estadoPaso4 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_EXAMENES
        assert(estados_pasos.estadoPaso5 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_DOCENTES

    def test_guardar_nuevas_respuestas_parciales_sobre_paso_en_curso_queda_en_curso(self):
        paso_actual = GRUPO_ENCUESTA_CONTENIDO

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]

        encuesta = EncuestaAlumno.query.first()

        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).first()

        assert(estados_pasos.estadoPaso1 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_GENERAL
        assert(estados_pasos.estadoPaso2 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CONTENIDO
        assert(estados_pasos.estadoPaso3 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CLASES
        assert(estados_pasos.estadoPaso4 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_EXAMENES
        assert(estados_pasos.estadoPaso5 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_DOCENTES

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual
        preguntas1 = [preguntas[0], preguntas[3],preguntas[6]]
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas1, self.get_datos_respuestas_default())
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert (len(preguntas1) == len(respuestas))

        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).first()

        assert(estados_pasos.estadoPaso1 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_GENERAL
        assert(estados_pasos.estadoPaso2 == PASO_ENCUESTA_EN_CURSO) #GRUPO_ENCUESTA_CONTENIDO
        assert(estados_pasos.estadoPaso3 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CLASES
        assert(estados_pasos.estadoPaso4 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_EXAMENES
        assert(estados_pasos.estadoPaso5 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_DOCENTES

        preguntas2 = [preguntas[0], preguntas[1]]
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas2, self.get_datos_respuestas_default())
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert (len(preguntas2) == len(respuestas))

        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).first()

        assert(estados_pasos.estadoPaso1 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_GENERAL
        assert(estados_pasos.estadoPaso2 == PASO_ENCUESTA_EN_CURSO) #GRUPO_ENCUESTA_CONTENIDO
        assert(estados_pasos.estadoPaso3 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CLASES
        assert(estados_pasos.estadoPaso4 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_EXAMENES
        assert(estados_pasos.estadoPaso5 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_DOCENTES

    def test_guardar_nuevas_respuestas_completas_sobre_paso_en_curso_queda_finalizado(self):
        paso_actual = GRUPO_ENCUESTA_CONTENIDO

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]

        encuesta = EncuestaAlumno.query.first()

        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).first()

        assert(estados_pasos.estadoPaso1 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_GENERAL
        assert(estados_pasos.estadoPaso2 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CONTENIDO
        assert(estados_pasos.estadoPaso3 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CLASES
        assert(estados_pasos.estadoPaso4 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_EXAMENES
        assert(estados_pasos.estadoPaso5 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_DOCENTES

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual
        preguntas1 = [preguntas[0], preguntas[3],preguntas[6]]
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas1, self.get_datos_respuestas_default())
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert (len(preguntas1) == len(respuestas))

        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).first()

        assert(estados_pasos.estadoPaso1 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_GENERAL
        assert(estados_pasos.estadoPaso2 == PASO_ENCUESTA_EN_CURSO) #GRUPO_ENCUESTA_CONTENIDO
        assert(estados_pasos.estadoPaso3 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CLASES
        assert(estados_pasos.estadoPaso4 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_EXAMENES
        assert(estados_pasos.estadoPaso5 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_DOCENTES

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, self.get_datos_respuestas_default())
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert (len(preguntas) == len(respuestas))

        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).first()

        assert(estados_pasos.estadoPaso1 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_GENERAL
        assert(estados_pasos.estadoPaso2 == PASO_ENCUESTA_FINALIZADO) #GRUPO_ENCUESTA_CONTENIDO
        assert(estados_pasos.estadoPaso3 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CLASES
        assert(estados_pasos.estadoPaso4 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_EXAMENES
        assert(estados_pasos.estadoPaso5 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_DOCENTES

    def test_guardar_respuestas_completas_en_categoria_docentes_guarda_correctamente_y_el_paso_queda_finalizado(self):
        paso_actual = GRUPO_ENCUESTA_DOCENTES

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]

        encuesta = EncuestaAlumno.query.first()

        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).first()

        assert(estados_pasos.estadoPaso1 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_GENERAL
        assert(estados_pasos.estadoPaso2 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CONTENIDO
        assert(estados_pasos.estadoPaso3 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CLASES
        assert(estados_pasos.estadoPaso4 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_EXAMENES
        assert(estados_pasos.estadoPaso5 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_DOCENTES

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            DOCENTE: {
                "docentes": [{
                    "id_docente": 1,
                    "comentario": "Este es un comentario de hasta 250 caracteres para un docente"
                }]
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert (len(preguntas) == len(respuestas))

        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).first()

        assert(estados_pasos.estadoPaso1 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_GENERAL
        assert(estados_pasos.estadoPaso2 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CONTENIDO
        assert(estados_pasos.estadoPaso3 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CLASES
        assert(estados_pasos.estadoPaso4 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_EXAMENES
        assert(estados_pasos.estadoPaso5 == PASO_ENCUESTA_FINALIZADO) #GRUPO_ENCUESTA_DOCENTES

    def test_guardar_respuestas_en_categoria_docentes_sin_datos_de_respuesta_deja_el_paso_finalizado(self):
        paso_actual = GRUPO_ENCUESTA_DOCENTES

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]

        encuesta = EncuestaAlumno.query.first()

        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).first()

        assert(estados_pasos.estadoPaso1 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_GENERAL
        assert(estados_pasos.estadoPaso2 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CONTENIDO
        assert(estados_pasos.estadoPaso3 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CLASES
        assert(estados_pasos.estadoPaso4 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_EXAMENES
        assert(estados_pasos.estadoPaso5 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_DOCENTES

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {})
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert (len(respuestas) == 0)

        estados_pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).first()

        assert(estados_pasos.estadoPaso1 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_GENERAL
        assert(estados_pasos.estadoPaso2 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CONTENIDO
        assert(estados_pasos.estadoPaso3 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_CLASES
        assert(estados_pasos.estadoPaso4 == PASO_ENCUESTA_NO_INICIADO) #GRUPO_ENCUESTA_EXAMENES
        assert(estados_pasos.estadoPaso5 == PASO_ENCUESTA_FINALIZADO) #GRUPO_ENCUESTA_DOCENTES

    def test_guardar_respuesta_de_tipo_texto_ya_guardada_la_sobreescribe(self):
        paso_actual = GRUPO_ENCUESTA_GENERAL

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[2]]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual

        texto_inicial = "Este es un texto libre de hasta 250 caracteres"
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            TEXTO_LIBRE: {
                "texto": texto_inicial
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert(len(respuestas) == 1)
        assert(respuestas['3']["texto"] == texto_inicial)

        texto_nuevo = "Este es un texto nuevo compuesto por varios caracteres pero diferente del anterior."
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            TEXTO_LIBRE: {
                "texto": texto_nuevo
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas_nuevas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert(len(respuestas_nuevas) == 1)
        assert(respuestas_nuevas['3']["texto"] == texto_nuevo)

    def test_guardar_respuesta_de_tipo_texto_con_texto_vacio_da_error(self):
        paso_actual = GRUPO_ENCUESTA_GENERAL

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[2]]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            TEXTO_LIBRE: {
                "texto": "                  "
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_guardar_respuesta_de_tipo_texto_con_texto_solo_con_simbolos_y_espacios_da_error(self):
        paso_actual = GRUPO_ENCUESTA_GENERAL

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[2]]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            TEXTO_LIBRE: {
                "texto": "  ?¿-+/*     !.   -        &$'()[] {},;."
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_guardar_respuesta_de_tipo_puntaje_ya_guardada_la_sobreescribe(self):
        paso_actual = GRUPO_ENCUESTA_CLASES

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[2]]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual

        puntaje_inicial = 4
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            PUNTAJE_1_A_5: {
                "puntaje": puntaje_inicial
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert(len(respuestas) == 1)
        assert(respuestas['27']["puntaje"] == puntaje_inicial)

        puntaje_nuevo = 2
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            PUNTAJE_1_A_5: {
                "puntaje": puntaje_nuevo
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas_nuevas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert(len(respuestas_nuevas) == 1)
        assert(respuestas_nuevas['27']["puntaje"] == puntaje_nuevo)

    def test_guardar_respuesta_de_tipo_puntaje_permite_puntajes_del_1_al_5_inclusives(self):
        paso_actual = GRUPO_ENCUESTA_CLASES

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[2]]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            PUNTAJE_1_A_5: {
                "puntaje": 1
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            PUNTAJE_1_A_5: {
                "puntaje": 2
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            PUNTAJE_1_A_5: {
                "puntaje": 3
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            PUNTAJE_1_A_5: {
                "puntaje": 4
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            PUNTAJE_1_A_5: {
                "puntaje": 5
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

    def test_guardar_respuesta_de_tipo_puntaje_0_da_error(self):
        paso_actual = GRUPO_ENCUESTA_CLASES

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[2]]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            PUNTAJE_1_A_5: {
                "puntaje": 0
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_guardar_respuesta_de_tipo_puntaje_negativo_da_error(self):
        paso_actual = GRUPO_ENCUESTA_CLASES

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[2]]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            PUNTAJE_1_A_5: {
                "puntaje": -1
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_guardar_respuesta_de_tipo_puntaje_mayor_a_cinco_da_error(self):
        paso_actual = GRUPO_ENCUESTA_CLASES

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[2]]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            PUNTAJE_1_A_5: {
                "puntaje": 6
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            PUNTAJE_1_A_5: {
                "puntaje": 10000
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_guardar_respuesta_de_tipo_puntaje_decimal_da_error(self):
        paso_actual = GRUPO_ENCUESTA_CLASES

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[2]]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            PUNTAJE_1_A_5: {
                "puntaje": 4.5
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)


    def test_guardar_respuesta_de_tipo_puntaje_vacio_da_error(self):
        paso_actual = GRUPO_ENCUESTA_CLASES

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[2]]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            PUNTAJE_1_A_5: {
                "puntaje": ""
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_guardar_respuesta_de_tipo_puntaje_datos_invalidos_da_error(self):
        paso_actual = GRUPO_ENCUESTA_CLASES

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[2]]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            PUNTAJE_1_A_5: {
                "puntaje": "pepe"
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_guardar_respuesta_de_tipo_numero_ya_guardada_la_sobreescribe(self):
        paso_actual = GRUPO_ENCUESTA_GENERAL

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[7]]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual

        numero_inicial = 15
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            NUMERO: {
                "numero": numero_inicial
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert(len(respuestas) == 1)
        assert(respuestas['9']["numero"] == numero_inicial)

        numero_nuevo = 89
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            NUMERO: {
                "numero": numero_nuevo
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas_nuevas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert(len(respuestas_nuevas) == 1)
        assert(respuestas_nuevas['9']["numero"] == numero_nuevo)

    def test_guardar_respuesta_de_tipo_numero_permite_numeros_entre_0_y_168_inclusives(self):
        paso_actual = GRUPO_ENCUESTA_GENERAL

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[7]]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual

        numero = 0
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            NUMERO: {
                "numero": numero
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert(len(respuestas) == 1)
        assert(respuestas['9']["numero"] == numero)

        numero = 168
        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            NUMERO: {
                "numero": numero
            }
        })
        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        respuestas = self.obtener_respuestas_guardadas_alumno(preguntas, encuesta, client)

        assert(len(respuestas) == 1)
        assert(respuestas['9']["numero"] == numero)

    def test_guardar_respuesta_de_tipo_numero_menor_que_cero_da_error(self):
        paso_actual = GRUPO_ENCUESTA_GENERAL

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[7]]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            NUMERO: {
                "numero": -1
            }
        })

        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_guardar_respuesta_de_tipo_numero_mayor_que_168_da_error(self):
        paso_actual = GRUPO_ENCUESTA_GENERAL

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[7]]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            NUMERO: {
                "numero": 169
            }
        })

        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_guardar_respuesta_de_tipo_numero_con_decimales_da_error(self):
        paso_actual = GRUPO_ENCUESTA_GENERAL

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[7]]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            NUMERO: {
                "numero": 85.5
            }
        })

        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_guardar_respuesta_de_tipo_numero_invalido_da_error(self):
        paso_actual = GRUPO_ENCUESTA_GENERAL

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[7]]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            NUMERO: {
                "numero": "pepe"
            }
        })

        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_guardar_respuesta_de_tipo_numero_vacio_da_error(self):
        paso_actual = GRUPO_ENCUESTA_GENERAL

        client = self.loguear_usuario()

        response = client.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, query_string={"categorias": paso_actual})
        preguntas = json.loads(response.get_data(as_text=True))["preguntas"]
        preguntas = [preguntas[7]]

        encuesta = EncuestaAlumno.query.first()

        parametros = {}
        parametros["id_encuesta"] = encuesta.id
        parametros["categoria"] = paso_actual

        parametros["respuestas"] = self.crear_respuestas_alumno(preguntas, {
            NUMERO: {
                "numero": ""
            }
        })

        response = client.get(GUARDAR_RESPUESTAS_ENCUESTA_ALUMNO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

        #Test con:
        # Datos invalidos / incompletos / incorrectos
        #  + Guardar respuestas que fueron guardadas previamente las sobreescribe
            #SI_NO = 2 --> Verificar que las subrespuestas sean borradas tambien
            #ESTRELLAS = 6
            #HORARIO = 3
            #DOCENTE = 4
            #CORRELATIVA = 5
            #TAG = 8
            #TEMATICA = 9
        # Preguntas con si/no que agregan en si pero la respuesta fue no se marcan como finalizado, idem invertido, idem pero no finalizado


if __name__ == '__main__':
    import unittest

    unittest.main()
