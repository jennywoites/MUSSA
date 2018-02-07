from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from flask import send_file
import os
from app.API_Rest.Services.GeneradorPDF import GeneradorPDF


class MateriasAlumnoPDFService(BaseService):
    def getNombreClaseServicio(self):
        return "Materias Alumno PDF Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    @login_required
    def put(self):
        carreras = self.obtener_lista("carreras")
        tipos_de_materias = self.obtener_lista("tipos_de_materias")

        alumno = self.obtener_alumno_usuario_actual()

        nombre_archivo = "Materias-" + alumno.get_padron() + ".pdf"
        ruta = os.path.join('tmp', nombre_archivo)

        self.generar_archivo_PDF(carreras, tipos_de_materias, alumno, nombre_archivo)

        return send_file(ruta, as_attachment=True)


    def generar_archivo_PDF(self, carreras, tipos_de_materias, alumno, nombre_archivo):
        ruta = os.path.join('app', 'tmp', nombre_archivo)
        generador = GeneradorPDF(ruta)

        generador.insertar_logos()
        generador.insertar_datos_alumno(alumno)

        MATERIAS_APROBADAS_Y_DESAPROBADAS = '0'
        MATERIAS_FINAL_PENDIENTE = '1'
        MATERIAS_EN_CURSO = '2'

        if MATERIAS_APROBADAS_Y_DESAPROBADAS in tipos_de_materias:
            generador.insertar_materias_rendidas(alumno, carreras)

        if MATERIAS_FINAL_PENDIENTE in tipos_de_materias:
            generador.insertar_materias_final_pendiente(alumno, carreras)

        if MATERIAS_EN_CURSO in tipos_de_materias:
            generador.insertar_materias_en_curso(alumno, carreras)

        generador.guardar_pdf()

#########################################
CLASE = MateriasAlumnoPDFService
URLS_SERVICIOS = (
    '/api/alumno/formulario/materias_alumno',
)
#########################################
