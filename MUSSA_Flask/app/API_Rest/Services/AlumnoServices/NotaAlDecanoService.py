from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from flask import send_file
import os


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
        email = self.obtener_texto_o_guion("email")

        alumno = self.obtener_alumno_usuario_actual()

        nombre_archivo = "NotaAlDecano-" + alumno.get_padron() + ".pdf"
        ruta = os.path.join('tmp', nombre_archivo)

        self.generar_archivo_PDF(objeto, motivo, telefono, domicilio, localidad, dni, anio_ingreso, email, alumno, ruta)

        return send_file(ruta, as_attachment=True)

    def obtener_texto_o_guion(self, nombre_parametro):
        texto = self.obtener_texto(nombre_parametro)
        return texto if texto else '-'

    def generar_archivo_PDF(self, objeto, motivo, telefono, domicilio, localidad, dni, anio_ingreso, email, alumno,
                            ruta):
        pass


#########################################
CLASE = NotaAlDecanoService
URLS_SERVICIOS = (
    '/api/alumno/formulario/nota_al_decano',
)
#########################################
