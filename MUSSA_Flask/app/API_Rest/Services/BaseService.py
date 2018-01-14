from flask_restful import Resource
import logging
from flask import request
from app.API_Rest.codes import *


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

    def validar_parametros(self, parametros):
        """
        Valida los parametros enviados. Devuelve una tupla con los siguientes valores:
        1) Si es valido True, caso contrario False.
        2) Mensaje. Si hay error este mensaje indica su causa.
        3) Código: Si no hay error devuelve -1. Si hay error devuelve el código de error de servicio (ej: 404)

        Recibe parámetros que es un diccionario con el siguiente formato:
        - clave: nombre del parametro a validar
        - valor: diccionario con los siguientes campos:
            - 'PARAMETRO': valor que toma el parametro
            - 'FUNCIONES_VALIDACION': diccionario con funciones:
                - clave: Nombre de la funcion de validacion
                - valor: Lista de parametros extras que recibe la funcion ademas del atributo. Si no recibe parametros
                        extras entonces la lista es una lista vacía.

        Ejemplo de invocación:

        parametros_son_validos, msj, codigo = self.validar_parametros({
            "idTematica": {
                "PARAMETRO": idTematica,
                "FUNCIONES_VALIDACION": {
                    self.id_es_valido: [],
                    self.existe_id: [TematicaMateria]
                }
            }
        })
        """
        for nombre_parametro in parametros:
            parametro = parametros[nombre_parametro]["PARAMETRO"]
            funciones_validacion = parametros[nombre_parametro]["FUNCIONES_VALIDACION"]
            for nombre_funcion_validacion in funciones_validacion:
                argumentos_funcion = [nombre_parametro, parametro] + funciones_validacion[nombre_funcion_validacion]
                es_valido, msj, codigo = nombre_funcion_validacion(*argumentos_funcion)
                if not es_valido:
                    return es_valido, msj, codigo
        return True, 'Todos los parámetros son válidos', -1


    def id_es_valido(self, nombre_parametro, id_a_validar):
        id_a_validar = str(id_a_validar)

        if not id_a_validar.isdigit():
            return False, 'El ' + nombre_parametro + 'no es un número entero', CLIENT_ERROR_BAD_REQUEST

        es_valido = int(id_a_validar) > 0
        msj, codigo = ('El ' + nombre_parametro + ' debe ser mayor a 0', CLIENT_ERROR_BAD_REQUEST) if not es_valido \
            else ('El ' + nombre_parametro + ' es valido', -1)

        return es_valido, msj, codigo


    def existe_id(self, nombre_parametro, id_clase, clase):
        elemento = clase.query.get(id_clase)

        msj, codigo = ('El ' + nombre_parametro + ' existe', -1) if elemento \
            else ('El ' + nombre_parametro + ' no existe', CLIENT_ERROR_NOT_FOUND)

        return elemento is not None, msj, codigo


    def booleano_es_valido(self, nombre_parametro, valor, obligatorio=False):
        msj_base = "El valor booleano " + nombre_parametro
        if not obligatorio and valor is None:
            return True, msj_base + ' no es requerido', -1

        msj, codigo = (msj_base + ' no es válido', -1) if valor is None \
            else (msj_base + ' es válido', CLIENT_ERROR_BAD_REQUEST)

        return valor is not None, msj, codigo

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
