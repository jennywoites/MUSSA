from app.API_Rest.codes import *
from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from app.models.generadorJSON.alumno_generadorJSON import generarJSON_materia_alumno
from app.models.carreras_models import Carrera
from app.models.alumno_models import MateriasAlumno
from app.DAO.MateriasDAO import *
import functools


class AllMateriasAlumnoService(BaseService):
    def getNombreClaseServicio(self):
        return "All Materias Alumno Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    @login_required
    def get(self):
        estados = self.obtener_lista("estados")
        estados_invalidos = [PENDIENTE]
        return self.obtener_materias_alumno_por_categorias(estados, estados_invalidos)

    def obtener_materias_alumno_por_categorias(self, estados, estados_invalidos, id_carrera=None):
        self.logg_parametros_recibidos()

        alumno = self.obtener_alumno_usuario_actual()

        if not alumno:
            msj = "El usuario no tiene ningun alumno asociado"
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_NOT_FOUND

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            ("estado", {
                self.PARAMETRO: estados,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.es_numero_valido, []),
                    (self.estado_materia_es_valido, [estados_invalidos])
                ]
            }),
            ("id_carrera", {
                self.PARAMETRO: id_carrera,
                self.ES_OBLIGATORIO: False,
                self.FUNCIONES_VALIDACION: [
                    (self.id_es_valido, []),
                    (self.existe_id, [Carrera])
                ]
            }),
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        estado = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[PENDIENTE]).first()

        query = MateriasAlumno.query.filter_by(alumno_id=alumno.id)
        query = query.filter(MateriasAlumno.estado_id == estado.id)

        materias = query.all()

        materias_alumno_result = []
        for materia_alumno in materias:
            materias_alumno_result.append(generarJSON_materia_alumno(materia_alumno))

        materias_alumno_result = sorted(materias_alumno_result, key=functools.cmp_to_key(cmp_materias_result))

        result = ({'materias_alumno': materias_alumno_result}, SUCCESS_OK)
        self.logg_resultado(result)

        return result

    def estado_materia_es_valido(self, nombre_parametro, valor, es_obligatorio, estados_invalidos):
        if not str(valor).isdigit():
            return (False, 'El estado {}debe ser un número'.format(valor), CLIENT_ERROR_BAD_REQUEST)

        estado = EstadoMateria.query.filter_by(
            estado=ESTADO_MATERIA[valor]).first() if valor in ESTADO_MATERIA else None
        if not estado:
            return (False, 'El estado {} no existe'.format(valor), CLIENT_ERROR_NOT_FOUND)

        return (True, 'El estado es válido', -1) if valor not in estados_invalidos \
            else (False, 'El estado {} es inválido'.format(valor), CLIENT_ERROR_BAD_REQUEST)


def cmp_materias_result(materia1, materia2):
    codigo1 = convertir_codigo(materia1)
    codigo2 = convertir_codigo(materia2)

    estado1 = materia1["estado"]
    estado2 = materia2["estado"]

    if estado1 == ESTADO_MATERIA[EN_CURSO]:
        if estado2 != ESTADO_MATERIA[EN_CURSO]:
            return 1
        return cmp_codigo(codigo1, codigo2)

    if estado2 == ESTADO_MATERIA[EN_CURSO]:
        return -1

    if estado1 == ESTADO_MATERIA[FINAL_PENDIENTE]:
        if estado2 != ESTADO_MATERIA[FINAL_PENDIENTE]:
            return 1
        return cmp_codigo(codigo1, codigo2)

    if estado2 == ESTADO_MATERIA[FINAL_PENDIENTE]:
        return -1

    if materia1["fecha_aprobacion"] < materia2["fecha_aprobacion"]:
        return -1
    elif materia1["fecha_aprobacion"] > materia2["fecha_aprobacion"]:
        return 1

    return cmp_codigo(codigo1, codigo2)


def cmp_codigo(codigo1, codigo2):
    if codigo1 < codigo2:
        return -1
    elif codigo1 > codigo2:
        return 1
    return 0


def convertir_codigo(materia):
    LONGITUD_CODIGO = 4
    codigo = materia["codigo"]
    return "0" * (LONGITUD_CODIGO - len(codigo)) + codigo


#########################################
CLASE = AllMateriasAlumnoService
URLS_SERVICIOS = (
    '/api/alumno/materia/all',
)
#########################################
