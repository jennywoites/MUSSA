from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from flask import send_file
import os
from app.API_Rest.Services.GeneradorPDF import GeneradorPDF


class NotaAlDecanoService(BaseService):
    def getNombreClaseServicio(self):
        return "Nota Al Decano Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    @login_required
    def put(self):
        objeto = self.obtener_texto_o_guion("objeto")
        motivo = self.obtener_texto_o_guion("motivo")
        telefono = self.obtener_texto_o_guion("telefono")
        domicilio = self.obtener_texto_o_guion("domicilio")
        localidad = self.obtener_texto_o_guion("localidad")
        dni = self.obtener_texto_o_guion("dni")
        anio_ingreso = self.obtener_texto_o_guion("anio_ingreso")
        nota_extendida = self.obtener_texto("nota_extendida")

        alumno = self.obtener_alumno_usuario_actual()

        nombre_archivo = "NotaAlDecano-" + alumno.get_padron() + ".pdf"
        ruta = os.path.join('tmp', nombre_archivo)

        self.generar_archivo_PDF(objeto, motivo, telefono, domicilio, localidad, dni, anio_ingreso, nota_extendida,
                                 alumno, nombre_archivo)

        return send_file(ruta, as_attachment=True)

    def generar_archivo_PDF(self, objeto, motivo, telefono, domicilio, localidad, dni, anio_ingreso, nota_extendida,
                            alumno, nombre_archivo):
        ruta = os.path.join('app', 'tmp', nombre_archivo)
        generador = GeneradorPDF(ruta)

        generador.insertar_logos()

        generador.insertar_datos_direccion_alumnos()
        generador.insertar_fecha_en_buenos_aires()

        generador.insertar_objeto(objeto)

        generador.insertar_dirigida_al_decano()
        generador.insertar_datos_alumnos_y_motivo(alumno, motivo)
        generador.insertar_informacion_adjunta()
        generador.insertar_despedida_formal()

        generador.insertar_firma_y_aclaracion()

        generador.insertar_informacion_contacto_alumno(alumno, telefono, domicilio, localidad, dni, anio_ingreso)

        generador.insertar_informacion_tramite()
        generador.insertar_info_depto_alumnos()

        if nota_extendida:
            generador.insertar_salto_de_pagina()
            generador.insertar_logos()
            generador.insertar_nota_extendida(nota_extendida)

        generador.insertar_salto_de_pagina()
        generador.insertar_logos()

        generador.insertar_materias_rendidas(alumno)
        generador.insertar_materias_final_pendiente(alumno)
        generador.insertar_materias_en_curso(alumno)

        generador.guardar_pdf()


#########################################
CLASE = NotaAlDecanoService
URLS_SERVICIOS = (
    '/api/alumno/formulario/nota_al_decano',
)
#########################################
