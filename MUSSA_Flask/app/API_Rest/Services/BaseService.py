from flask_restful import Resource
import logging
from flask import request


class BaseService(Resource):
    def getNombreClaseServicio(self):
        raise NotImplementedError("Todas las clases hijas deben tener un nombre. "
                                  "El nombre se identifica como 'Nombre de la Clase Service'")

    def obtener_argumentos(self):
        return request.args if request.args else request.form

    def obtener_parametro(self, nombre_parametro):
        datos = self.obtener_argumentos()
        return datos[nombre_parametro] if nombre_parametro in datos else None

    def generar_JSON_lista_datos(self, funcion_generadora_JSON, lista_datos):
        resultados_JSON = []
        for modelo_datos in lista_datos:
            resultados_JSON.append(funcion_generadora_JSON(modelo_datos))
        return resultados_JSON

    ##########################################################
    ##                      Loggin                          ##
    ##########################################################

    def logg_parametros_recibidos(self):
        argumentos = self.obtener_argumentos()
        msj = "No recibió parámetros" if not argumentos else "Recibió como parámetros --> {}".format(argumentos)
        logging.info(self.getNombreClaseServicio() + msj)

    def logg_resultado(self, resultado):
        logging.info(self.getNombreClaseServicio() + ': Resultado: {}'.format(resultado))

    def logg_error(self, msj):
        logging.error(self.getNombreClaseServicio() + ': ' + msj)

    ##########################################################
    ##            Obtener Paramteros por Tipo               ##
    ##########################################################

    def obtener_booleano(self, nombre_campo):
        """Devuelve True o False segun el dato del campo.
           Si el campo no existe o es invalido devuelve None"""

        valor = self.obtener_parametro(nombre_campo)
        if valor is None:
            return valor
        valor = valor.upper()

        if valor == 'TRUE':
            return True
        if valor == 'FALSE':
            return False

        return None

    ##########################################################
    ##                      Validaciones                    ##
    ##########################################################

    def booleano_es_valido(self, valor, obligatorio=False):
        if not obligatorio and valor is None:
            return True

        return valor is not None

#######################################################################################################################
# Todos los servicios requieren tener los siguientes campos definidos al finalizar la declaracion de la clase.        #
#                                                                                                                     #
# CLASE = AllTematicasService --> Nombre de la clase. El nombre de la clase y del archivo debe ser el mismo            #
#                                                                                                                     #
# URLS_SERVICIOS = ( --> Todas las urls que se registran para esa clase. Por ejemplo si el get recibe el id pero el    #
#                       post no lo hace se debe registrar la clase con ambas urls                                     #
#    '/api/tematica/id',                                                                                              #
#    '/api/tematica',                                                                                                 #
# )                                                                                                                    #
#######################################################################################################################
