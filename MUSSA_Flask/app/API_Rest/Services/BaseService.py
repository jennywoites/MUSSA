from flask_restful import Resource
import logging
from flask import request
from app.API_Rest.codes import *
import json
from flask_user import current_user
from app.models.alumno_models import Alumno
from app.models.carreras_models import Materia
from app import db
from app.utils import DIAS, convertir_horario
from flask_user import current_user


class BaseService(Resource):
    def getNombreClaseServicio(self):
        raise NotImplementedError("Todas las clases hijas deben tener un nombre. "
                                  "El nombre se identifica como 'Nombre de la Clase Service'")

    def obtener_argumentos(self):
        return request.args if request.args else request.form

    def obtener_parametro(self, nombre_parametro):
        datos = self.obtener_argumentos()
        return datos[nombre_parametro] if nombre_parametro in datos else None

    def obtener_alumno_usuario_actual(self):
        """
        Obtiene el alumno para el usuario actual.
        Si el alumno aún no fue creado lo crea.
        """
        alumno = Alumno.query.filter_by(user_id=current_user.id).first()
        if not alumno:
            alumno = Alumno(user_id=current_user.id)
            db.session.add(alumno)
            db.session.commit()
        return alumno

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

    def obtener_texto(self, nombre_campo):
        """
        Devuelve el dato del campo en formato string.
        Si el campo no existe devuelve None.
        """
        return self.obtener_parametro(nombre_campo)

    def obtener_lista(self, nombre_campo):
        """
        Devuelve una lista decodificada.
        Si el campo no existe devuelve una lista vacía
        """
        try:
            l_valores = self.obtener_parametro(nombre_campo)
            lista_decodificada = json.loads(l_valores)
            return lista_decodificada
        except:
            return []

    def obtener_lista_de_horarios(self, nombre_campo):
        """
        Devuelve una lista de horarios decodificada.
        Para cada hora reloj, la transforma en el horario
        decimal correspondiente. Si no puede trasnformarlo,
        lo deja en None.
        Si el campo no existe devuelve una lusta vacía.
        """
        l_horarios = self.obtener_lista(nombre_campo)
        for horario in l_horarios:
            horario["dia"] = horario["dia"].upper()
            horario["hora_desde"] = self.aux_convertir_horario(horario["hora_desde"])
            horario["hora_hasta"] = self.aux_convertir_horario(horario["hora_hasta"])

        return l_horarios

    def aux_convertir_horario(self, horario_a_convertir):
        try:
            nuevo_horario = convertir_horario(*horario_a_convertir.split(":"))
            return nuevo_horario
        except:
            return None

    ##########################################################
    ##                      Validaciones                    ##
    ##########################################################

    PARAMETRO = "PARAMETRO"
    FUNCIONES_VALIDACION = "FUNCIONES_VALIDACION"
    ES_OBLIGATORIO = "ES_OBLIGATORIO"

    def validar_parametros(self, parametros):
        """
        Valida los parametros enviados. Devuelve una tupla con los siguientes valores:
        1) Si es valido True, caso contrario False.
        2) Mensaje. Si hay error este mensaje indica su causa.
        3) Código: Si no hay error devuelve -1. Si hay error devuelve el código de error de servicio (ej: 404)

        Recibe 'parametros' que es un diccionario con el siguiente formato:
        - clave: nombre del parametro a validar
        - valor: diccionario con los siguientes campos:
            - 'PARAMETRO': valor que toma el parametro
            - 'FUNCIONES_VALIDACION': lista con funciones. La lista de funciones se ejectura en orden.
                Las funciones se organizan como tuplas donde la posición es:
                - Pos 0: Nombre de la funcion de validacion
                - Pos 1: Lista de parametros extras que recibe la funcion ademas del atributo. Si no recibe parametros
                        extras entonces la lista es una lista vacía. Los parámetros extras son todos aquellos luego de:
                        'nombre_parametro', 'valor', 'es_obligatorio'

        * En caso de que el parámetro sea una lista o tupla se aplicarán las funciones de validación a cada elemento
         de la tupla o lista

        Ejemplo de invocación:

        parametros_son_validos, msj, codigo = self.validar_parametros({
            "idTematica": {
                "PARAMETRO": idTematica,
                "ES_OBLIGATORIO": False,
                "FUNCIONES_VALIDACION": [
                    (self.id_es_valido, []),
                    (self.existe_id, [TematicaMateria])
                ]
            }
        })
        """
        for nombre_parametro in parametros:
            parametro_o_lista = parametros[nombre_parametro][self.PARAMETRO]

            elementos_a_evaluar = [parametro_o_lista] if not isinstance(parametro_o_lista, (list, tuple)) \
                else parametro_o_lista

            es_obligatorio = parametros[nombre_parametro][self.ES_OBLIGATORIO]
            funciones_validacion = parametros[nombre_parametro][self.FUNCIONES_VALIDACION]

            for i in range(len(elementos_a_evaluar)):
                parametro = elementos_a_evaluar[i]
                nombre_parametro_actual = nombre_parametro if (len(elementos_a_evaluar) == 1) \
                    else (nombre_parametro + "-" + str(i))

                NOMBRE_FUNCION = 0
                PARAMETROS_EXTRAS = 1
                for datos_funciones_validacion in funciones_validacion:
                    nombre_funcion_validacion = datos_funciones_validacion[NOMBRE_FUNCION]
                    argumentos_base = [nombre_parametro_actual, parametro, es_obligatorio]
                    argumentos_funcion = argumentos_base + datos_funciones_validacion[PARAMETROS_EXTRAS]
                    es_valido, msj, codigo = nombre_funcion_validacion(*argumentos_funcion)
                    if not es_valido:
                        return es_valido, msj, codigo

        return True, 'Todos los parámetros son válidos', -1

    def mensaje_campo_no_obligatorio(self, nombre_parametro):
        return True, 'El ' + nombre_parametro + ' no existe pero no es obligatorio', -1

    def padron_es_valido(self, nombre_parametro, padron, es_obligatorio, id_alumno):
        msj_valido = 'El padron {} es valido'.format(padron)
        msj_invalido = 'El padron {} no es valido'.format(padron)

        if not padron and es_obligatorio:
            return False, msj_invalido, CLIENT_ERROR_NOT_FOUND

        if not padron:
            return True, msj_valido, -1

        LONGITUD_MINIMA_PADRON = 5
        LONGITUD_MAXIMA_PADRON = 7
        if not padron.isdigit() or not (LONGITUD_MINIMA_PADRON <= len(padron) <= LONGITUD_MAXIMA_PADRON):
            return False, msj_invalido, CLIENT_ERROR_BAD_REQUEST

        msj_invalido = 'El padron {} ya existe'.format(padron)
        es_valido = (len(Alumno.query.filter_by(padron=padron).filter(Alumno.id.isnot(id_alumno)).all()) == 0)
        return (True, msj_valido, -1) if es_valido else (False, msj_invalido, CLIENT_ERROR_BAD_REQUEST)

    def id_es_valido(self, nombre_parametro, id_a_validar, es_obligatorio):
        if not id_a_validar and not es_obligatorio:
            return self.mensaje_campo_no_obligatorio(nombre_parametro)

        id_a_validar = str(id_a_validar)

        if not id_a_validar.isdigit():
            return False, 'El ' + nombre_parametro + 'no es un número entero', CLIENT_ERROR_BAD_REQUEST

        es_valido = int(id_a_validar) > 0
        msj, codigo = ('El ' + nombre_parametro + ' debe ser mayor a 0', CLIENT_ERROR_BAD_REQUEST) if not es_valido \
            else ('El ' + nombre_parametro + ' es valido', -1)

        return es_valido, msj, codigo

    def horario_es_valido(self, nombre_parametro, valor, es_obligatorio):
        dia = valor["dia"]
        hora_desde = valor["hora_desde"]
        hora_hasta = valor["hora_hasta"]

        if not dia in DIAS:
            return False, 'El dia {} de {} no es un día válido'.format(dia, nombre_parametro), CLIENT_ERROR_BAD_REQUEST

        es_valido = (hora_desde is not None and hora_hasta is not None)

        msj, codigo = ('Las horas desde/hasta de {} contienen errores'.format(nombre_parametro),
                       CLIENT_ERROR_BAD_REQUEST) if not es_valido else (
            'El parametro {} está correcto'.format(nombre_parametro), -1)

        return es_valido, msj, codigo

    def existe_id(self, nombre_parametro, id_clase, es_obligatorio, clase):
        if not id_clase and not es_obligatorio:
            return self.mensaje_campo_no_obligatorio(nombre_parametro)

        elemento = clase.query.get(id_clase)

        msj, codigo = ('El ' + nombre_parametro + ' existe', -1) if elemento \
            else ('El ' + nombre_parametro + ' no existe', CLIENT_ERROR_NOT_FOUND)

        return elemento is not None, msj, codigo

    def booleano_es_valido(self, nombre_parametro, valor, es_obligatorio):
        if not es_obligatorio and valor is None:
            return self.mensaje_campo_no_obligatorio(nombre_parametro)

        msj_base = "El valor booleano " + nombre_parametro
        msj, codigo = (msj_base + ' no es válido', -1) if valor is not None \
            else (msj_base + ' es válido', CLIENT_ERROR_BAD_REQUEST)

        return valor is not None, msj, codigo

    def validar_contenido_y_longitud_texto(self, nombre_parametro, valor, es_obligatorio, len_min, len_max):
        if not es_obligatorio and valor is None:
            return self.mensaje_campo_no_obligatorio(nombre_parametro)

        for simbolo in "¡!,.-¿?*/+-'[]{}() &%$|@#~¬=;:\n":
            valor = valor.replace(simbolo, '')

        es_valido = (len_min <= len(valor) <= len_max)
        msj, codigo = ("El texto de {} debe tener al menos {} caracteres, y tener una logitud "
                       "menor a {} caracteres".format(nombre_parametro, len_min, len_max), CLIENT_ERROR_BAD_REQUEST) \
            if not es_valido else ('El texto de ' + nombre_parametro + ' es valido.', -1)

        return es_valido, msj, codigo

    def es_numero_valido(self, nombre_parametro, valor, es_obligatorio):
        if not es_obligatorio and valor is None:
            return self.mensaje_campo_no_obligatorio(nombre_parametro)

        es_valido = str(valor).isdigit()

        msj, codigo = ("El {} no es un número".format(nombre_parametro), CLIENT_ERROR_BAD_REQUEST) if not es_valido \
            else ("El {} es un número válido".format(nombre_parametro), -1)

        return es_valido, msj, codigo

    def existe_el_elemento(self, nombre_parametro, valor, es_obligatorio, clase, propiedad):
        if not es_obligatorio and valor is None:
            return self.mensaje_campo_no_obligatorio(nombre_parametro)

        es_valido = len(clase.query.filter(propiedad == valor).all()) > 0

        msj, codigo = ("El {} no existe".format(nombre_parametro), CLIENT_ERROR_NOT_FOUND) if not es_valido \
            else ("El {} existe".format(nombre_parametro), -1)

        return es_valido, msj, codigo

    def existe_elemento_que_comienza_con_el_valor(self, nombre_parametro, valor, es_obligatorio, clase, propiedad):
        if not es_obligatorio and valor is None:
            return self.mensaje_campo_no_obligatorio(nombre_parametro)

        es_valido = len(clase.query.filter(propiedad.like(str(valor) + "%")).all()) > 0

        msj, codigo = ("El {} no existe".format(nombre_parametro), CLIENT_ERROR_NOT_FOUND) if not es_valido \
            else ("El {} existe".format(nombre_parametro), -1)

        return es_valido, msj, codigo

    ##########################################################
    ##             Servicios Base de las Entidades          ##
    ##########################################################

    def servicio_get_base(self, idClase, nombreParametro, clase, funcion_generador_JSON):
        self.logg_parametros_recibidos()

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            self.get_validaciones_entidad_basica(nombreParametro, idClase, clase)
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        instancia_buscada = clase.query.get(idClase)

        result = (funcion_generador_JSON(instancia_buscada), SUCCESS_OK)
        self.logg_resultado(result)

        return result

    def servicio_delete_base(self, idClase, nombreParametro, clase):
        self.logg_parametros_recibidos()

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            self.get_validaciones_entidad_basica(nombreParametro, idClase, clase)
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        clase.query.filter_by(id=idClase).delete()
        db.session.commit()

        result = SUCCESS_NO_CONTENT
        self.logg_resultado(result)

        return result

    ##########################################################
    ##           Formato de validaciones generales          ##
    ##########################################################

    def get_validaciones_entidad_basica(self, nombreParametro, idClase, clase, es_obligatorio=True):
        return (nombreParametro, {
            self.PARAMETRO: idClase,
            self.ES_OBLIGATORIO: es_obligatorio,
            self.FUNCIONES_VALIDACION: [
                (self.id_es_valido, []),
                (self.existe_id, [clase])
            ]
        })

    def get_validaciones_codigo_materia(self, nombreParametro, valor, obligatorio):
        return (nombreParametro, {
            self.PARAMETRO: valor,
            self.ES_OBLIGATORIO: obligatorio,
            self.FUNCIONES_VALIDACION: [
                (self.es_numero_valido, []),
                (self.existe_elemento_que_comienza_con_el_valor, [Materia, Materia.codigo])
            ]
        })

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
