from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from flask import send_file
import os
from app.API_Rest.Services.GeneradorPDF import GeneradorPDF
from app.API_Rest.codes import *
from app.models.carreras_models import Carrera


class MateriasAlumnoPDFService(BaseService):
    def getNombreClaseServicio(self):
        return "Materias Alumno PDF Service"

    MATERIAS_APROBADAS_Y_DESAPROBADAS = '0'
    MATERIAS_FINAL_PENDIENTE = '1'
    MATERIAS_EN_CURSO = '2'

    ##########################################
    ##                Servicios             ##
    ##########################################

    @login_required
    def put(self):
        alumno = self.obtener_alumno_usuario_actual()

        if not alumno:
            msj = "El usuario no tiene ningun alumno asociado"
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_NOT_FOUND

        carreras = self.obtener_lista("carreras")
        tipos_de_materias = self.obtener_lista("tipos_de_materias")

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            ("carreras", {
                self.PARAMETRO: carreras,
                self.ES_OBLIGATORIO: False,
                self.FUNCIONES_VALIDACION: [
                    (self.id_es_valido, []),
                    (self.existe_id, [Carrera])
                ]
            }),
            ("tipos_de_materias", {
                self.PARAMETRO: tipos_de_materias,
                self.ES_OBLIGATORIO: False,
                self.FUNCIONES_VALIDACION: [
                    (self.tipo_de_materia_es_valido, [])
                ]
            })
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        nombre_archivo = "Materias-" + alumno.get_padron() + ".pdf"
        ruta = os.path.join('tmp', nombre_archivo)

        self.generar_archivo_PDF(carreras, tipos_de_materias, alumno, nombre_archivo)

        return send_file(ruta, as_attachment=True)

    def generar_archivo_PDF(self, carreras, tipos_de_materias, alumno, nombre_archivo):
        ruta = os.path.join('app', 'tmp', nombre_archivo)
        generador = GeneradorPDF(ruta)

        generador.insertar_logos()
        generador.insertar_datos_alumno(alumno)

        if self.MATERIAS_APROBADAS_Y_DESAPROBADAS in tipos_de_materias:
            generador.insertar_materias_rendidas(alumno, carreras)

        if self.MATERIAS_FINAL_PENDIENTE in tipos_de_materias:
            generador.insertar_materias_final_pendiente(alumno, carreras)

        if self.MATERIAS_EN_CURSO in tipos_de_materias:
            generador.insertar_materias_en_curso(alumno, carreras)

        generador.guardar_pdf()

    def tipo_de_materia_es_valido(self, nombre_parametro, valor, es_obligatorio):
        try:
            int(str(valor))
        except:
            return False, 'El {} no es un entero'.format(nombre_parametro), CLIENT_ERROR_BAD_REQUEST

        valores_validos = [
            self.MATERIAS_APROBADAS_Y_DESAPROBADAS,
            self.MATERIAS_FINAL_PENDIENTE,
            self.MATERIAS_EN_CURSO
        ]

        es_valido = valor in valores_validos
        if es_valido:
            return self.mensaje_OK(nombre_parametro)

        return False, 'El {} debe ser un numero de los siguientes: {}'.format(nombre_parametro, valores_validos), \
               CLIENT_ERROR_BAD_REQUEST


#########################################
CLASE = MateriasAlumnoPDFService
URLS_SERVICIOS = (
    '/api/alumno/formulario/materias_alumno',
)
#########################################
