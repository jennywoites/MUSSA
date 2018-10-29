from app.API_Rest.GeneradorPlanCarreras.Constantes import *
from app.utils import cmp_to_key
from app.API_Rest.GeneradorPlanCarreras.modelos.Materia import Materia
from app.API_Rest.GeneradorPlanCarreras.modelos.Curso import Curso
import hashlib

CREDITOS_MINIMOS_ELECTIVAS = 5
NUM_EJEMPLO_MATERIAS = 4

ARCHIVO_PULP = "pulp_generado.py"
ARCHIVO_PULP_OPTIMIZADO = "pulp_optimizado.py"
ARCHIVO_RESULTADO_PULP = "resultados_pulp_001.csv"

DIAS = [LUNES, MARTES, MIERCOLES, JUEVES, VIERNES, SABADO]

FRANJA_MIN = 1  # Corresponde al horario de 07:00 a 07:30 --> 1
FRANJA_MAX = 33  # Corresponde al horario de 23:00 a 23:30 --> 33

MAX_CUATRIMESTRES_TOTALES = 10
MAX_CANTIDAD_MATERIAS_POR_CUATRIMESTRE = 3


class Parametros:
    def __init__(self):
        self.set_valores_default()

    def set_valores_default(self):
        # Si el primer cuatrimestre es 1 entonces es True.
        # Si el primer cuatrimestres es 2 entonces es False
        self.primer_cuatrimestre_es_impar = True

        self.plan = {}
        self.materias = {}
        self.horarios = {}
        self.horarios_no_permitidos = []
        self.creditos_minimos_electivas = CREDITOS_MINIMOS_ELECTIVAS

        self.nombre_archivo_pulp = ARCHIVO_PULP
        self.nombre_archivo_resultados_pulp = ARCHIVO_RESULTADO_PULP
        self.nombre_archivo_pulp_optimizado = ARCHIVO_PULP_OPTIMIZADO

        self.set_franjas(FRANJA_MIN, FRANJA_MAX)
        self.dias = DIAS
        self.max_cuatrimestres = MAX_CUATRIMESTRES_TOTALES
        self.max_cant_materias_por_cuatrimestre = MAX_CANTIDAD_MATERIAS_POR_CUATRIMESTRE

        self.materias_CBC_pendientes = []
        self.orientacion = ''
        self.id_carrera = ''
        self.cuatrimestre_minimo_para_materia = {}
        self.creditos_minimos_tematicas = {}
        self.cuatrimestre_inicio = 1
        self.anio_inicio = '2018'
        self.materias_incompatibles = {}

        # Los valores son en medias horas, por lo que si se quiere una hora maxima, se guardan 2
        self.max_horas_cursada = 0
        self.max_horas_extras = 0

        # Estas materias son largas y se las divide en dos cuatrimestres pero es la misma materia
        self.materia_trabajo_final = []

        self.plan_generado = []
        self.id_plan_estudios = -1
        self.estado_plan_de_estudios = -1

        self.user_id = -1

        # Creditos en materias aprobadas / que se daran por aprobadas antes de la confeccion del plan de estudios
        self.creditos_preacumulados = 0

        self.hash_precalculado = ""

    def __str__(self):
        SALTO = "\n"
        parametros = "{" + SALTO
        parametros += "primer_cuatrimestre_es_impar: " + str(self.primer_cuatrimestre_es_impar) + SALTO

        parametros += "Plan: {" + SALTO
        for id_materia in self.plan:
            parametros += "{}: {}".format(id_materia, self.plan[id_materia]) + SALTO
        parametros += "}" + SALTO

        parametros += "Materias: {" + SALTO
        for id_materia in self.materias:
            parametros += str(id_materia) + ": " + SALTO
            parametros += str(self.materias[id_materia]) + SALTO
        parametros += "}" + SALTO

        parametros += "Horarios: {" + SALTO
        for id_materia in self.horarios:
            parametros += str(id_materia) + ": [" + SALTO
            for curso in self.horarios[id_materia]:
                parametros += str(curso) + SALTO
            parametros += "]" + SALTO
        parametros += "}" + SALTO

        parametros += "horarios_no_permitidos: " + str(self.horarios_no_permitidos) + SALTO
        parametros += "creditos_minimos_electivas: " + str(self.creditos_minimos_electivas) + SALTO

        parametros += "nombre_archivo_pulp: " + self.nombre_archivo_pulp + SALTO
        parametros += "nombre_archivo_resultados_pulp: " + self.nombre_archivo_resultados_pulp + SALTO
        parametros += "nombre_archivo_pulp_optimizado: " + self.nombre_archivo_pulp_optimizado + SALTO

        parametros += "franja_minima: " + str(self.franja_minima) + SALTO
        parametros += "franja_maxima: " + str(self.franja_maxima) + SALTO
        parametros += "dias: " + str(self.dias) + SALTO

        parametros += "max_cuatrimestres: " + str(self.max_cuatrimestres) + SALTO
        parametros += "max_cant_materias_por_cuatrimestre: " + str(self.max_cant_materias_por_cuatrimestre) + SALTO

        parametros += "materias_CBC_pendientes: " + str(self.materias_CBC_pendientes) + SALTO

        parametros += "orientacion: " + str(self.orientacion) + SALTO
        parametros += "id_carrera: " + str(self.id_carrera) + SALTO

        parametros += "cuatrimestre_minimo_para_materia: {" + SALTO
        for id_materia in self.cuatrimestre_minimo_para_materia:
            parametros += str(id_materia) + ": " + str(self.cuatrimestre_minimo_para_materia[id_materia]) + SALTO
        parametros += "}" + SALTO

        parametros += "creditos_minimos_tematicas: {" + SALTO
        for id_tematica in self.creditos_minimos_tematicas:
            parametros += str(id_tematica) + ": " + str(self.creditos_minimos_tematicas[id_tematica]) + SALTO
        parametros += "}" + SALTO

        parametros += "cuatrimestre_inicio: " + str(self.cuatrimestre_inicio) + SALTO
        parametros += "anio_inicio: " + str(self.anio_inicio) + SALTO

        parametros += "materias_incompatibles: {" + SALTO
        for id_materia in self.materias_incompatibles:
            parametros += str(id_materia) + ": " + str(self.materias_incompatibles[id_materia]) + SALTO
        parametros += "}" + SALTO

        parametros += "max_horas_cursada: " + str(self.max_horas_cursada) + SALTO
        parametros += "max_horas_extras: " + str(self.max_horas_extras) + SALTO

        parametros += "materia_trabajo_final: [" + SALTO
        for materia in self.materia_trabajo_final:
            parametros += str(materia.id_materia) + ": " + str(materia) + SALTO
        parametros += "]" + SALTO

        parametros += "id_plan_estudios:" + str(self.id_plan_estudios)
        parametros += "estado_plan_de_estudios:" + str(self.estado_plan_de_estudios)

        parametros += "id_usuario: " + str(self.user_id)

        parametros += "creditos_preacumulados:" + str(self.creditos_preacumulados)
        parametros += "hash_precalculado:" + self.hash_precalculado

        return parametros

    def obtener_hash_parametros_relevantes(self):
        ids_materias = sorted(list(self.plan.keys()))

        SEPARADOR = "|||"
        parametros = "primer_cuatrimestre_es_impar: " + str(self.primer_cuatrimestre_es_impar) + SEPARADOR

        parametros += "Plan: {"
        for id_materia in ids_materias:
            parametros += "{}: {};".format(id_materia, sorted(self.plan[id_materia]))
        parametros += "}" + SEPARADOR

        parametros += "Materias: {"
        for id_materia in ids_materias:
            parametros += "{}: {};".format(id_materia, self.materias[id_materia].obtener_hash_materia().hexdigest())
        parametros += "}" + SEPARADOR

        parametros += "Horarios: {"
        for id_materia in ids_materias:
            parametros += str(id_materia) + ": ["
            for curso in sorted(self.horarios[id_materia], key=lambda curso: curso.id_curso):
                parametros += curso.obtener_hash_curso().hexdigest()
            parametros += "]"
        parametros += "}" + SEPARADOR

        parametros += "creditos_minimos_electivas: " + str(self.creditos_minimos_electivas) + SEPARADOR
        parametros += "max_cant_materias_por_cuatrimestre: " + str(self.max_cant_materias_por_cuatrimestre) + SEPARADOR
        parametros += "materias_CBC_pendientes: " + str(self.materias_CBC_pendientes) + SEPARADOR

        parametros += "orientacion: " + str(self.orientacion) + SEPARADOR
        parametros += "id_carrera: " + str(self.id_carrera) + SEPARADOR

        parametros += "cuatrimestre_minimo_para_materia: {"
        for id_materia in sorted(list(self.cuatrimestre_minimo_para_materia.keys())):
            parametros += "{}: {};".format(id_materia, self.cuatrimestre_minimo_para_materia[id_materia])
        parametros += "}" + SEPARADOR

        parametros += "creditos_minimos_tematicas: {"
        for id_tematica in sorted(list(self.creditos_minimos_tematicas.keys())):
            parametros += "{}: {};".format(id_tematica, self.creditos_minimos_tematicas[id_tematica])
        parametros += "}" + SEPARADOR

        parametros += "materias_incompatibles: {"
        for id_materia in sorted(list(self.materias_incompatibles.keys())):
            parametros += "{}: {};".format(id_materia, sorted(self.materias_incompatibles[id_materia]))
        parametros += "}" + SEPARADOR

        parametros += "max_horas_cursada: " + str(self.max_horas_cursada) + SEPARADOR
        parametros += "max_horas_extras: " + str(self.max_horas_extras) + SEPARADOR

        parametros += "materia_trabajo_final: ["
        for materia in sorted(self.materia_trabajo_final, key=lambda materia: materia.codigo):
            parametros += materia.obtener_hash_materia().hexdigest() + "; "
        parametros += "]" + SEPARADOR

        parametros += "creditos_preacumulados:" + str(self.creditos_preacumulados)

        return hashlib.sha1(parametros.encode('utf-8'))

    def actualizar_valores_desde_JSON(self, parametros_JSON):
        self.primer_cuatrimestre_es_impar = parametros_JSON["primer_cuatrimestre_es_impar"]

        self.plan = {}
        for id_materia in parametros_JSON["plan"]:
            correlativas = []
            for id_correlativa in parametros_JSON["plan"][id_materia]:
                correlativas.append(int(id_correlativa))
            self.plan[int(id_materia)] = correlativas

        self.materias = {}
        for id_materia in parametros_JSON["materias"]:
            self.materias[int(id_materia)] = Materia(datos_JSON=parametros_JSON["materias"][id_materia])

        self.horarios = {}
        for id_materia in parametros_JSON["horarios"]:
            cursos = []
            for datos_curso in parametros_JSON["horarios"][id_materia]:
                cursos.append(Curso(datos_JSON=datos_curso))
            self.horarios[int(id_materia)] = cursos

        self.creditos_minimos_electivas = int(parametros_JSON["creditos_minimos_electivas"])

        self.nombre_archivo_pulp = parametros_JSON["nombre_archivo_pulp"]
        self.nombre_archivo_resultados_pulp = parametros_JSON["nombre_archivo_resultados_pulp"]
        self.nombre_archivo_pulp_optimizado = parametros_JSON["nombre_archivo_pulp_optimizado"]

        self.franja_minima = int(parametros_JSON["franja_minima"])
        self.franja_maxima = int(parametros_JSON["franja_maxima"])
        self.dias = parametros_JSON["dias"]

        self.max_cuatrimestres = int(parametros_JSON["max_cuatrimestres"])
        self.max_cant_materias_por_cuatrimestre = int(parametros_JSON["max_cant_materias_por_cuatrimestre"])

        self.materias_CBC_pendientes = []
        for id_materia in parametros_JSON["materias_CBC_pendientes"]:
            self.materias_CBC_pendientes.append(int(id_materia))

        self.orientacion = parametros_JSON["orientacion"]
        self.id_carrera = int(parametros_JSON["id_carrera"])

        self.cuatrimestre_minimo_para_materia = {}
        for id_materia in parametros_JSON["cuatrimestre_minimo_para_materia"]:
            self.cuatrimestre_minimo_para_materia[int(id_materia)] = int(
                parametros_JSON["cuatrimestre_minimo_para_materia"][id_materia])

        self.creditos_minimos_tematicas = {}
        for id_tematica in parametros_JSON["creditos_minimos_tematicas"]:
            self.creditos_minimos_tematicas[int(id_tematica)] = int(
                parametros_JSON["creditos_minimos_tematicas"][id_tematica])

        self.cuatrimestre_inicio = int(parametros_JSON["cuatrimestre_inicio"])
        self.anio_inicio = parametros_JSON["anio_inicio"]

        self.materias_incompatibles = {}
        for id_materia in parametros_JSON["materias_incompatibles"]:
            l_materias = []
            for id_materia_incompt in parametros_JSON["materias_incompatibles"][id_materia]:
                l_materias.append(int(id_materia_incompt))
            self.materias_incompatibles[int(id_materia)] = l_materias

        self.max_horas_cursada = int(parametros_JSON["max_horas_cursada"])
        self.max_horas_extras = int(parametros_JSON["max_horas_extras"])

        self.materia_trabajo_final = []
        for datos_materia in parametros_JSON["materia_trabajo_final"]:
            self.materia_trabajo_final.append(Materia(datos_JSON=datos_materia))

        self.plan_generado = []
        for cuatrimestre_plan in parametros_JSON["plan_generado"]:
            cuatrimeste = {}
            for id_materia in cuatrimestre_plan:
                cuatrimeste[int(id_materia)] = int(cuatrimestre_plan[id_materia])
            self.plan_generado.append(cuatrimeste)

        self.id_plan_estudios = int(parametros_JSON["id_plan_estudios"])
        self.estado_plan_de_estudios = int(parametros_JSON["estado_plan_de_estudios"])

        self.user_id = int(parametros_JSON["user_id"])

        self.creditos_preacumulados = int(parametros_JSON["creditos_preacumulados"])
        self.hash_precalculado = parametros_JSON["hash_precalculado"]

    def generar_parametros_json(self):
        parametros_JSON = {}
        parametros_JSON["primer_cuatrimestre_es_impar"] = self.primer_cuatrimestre_es_impar

        parametros_JSON["plan"] = dict(self.plan)

        parametros_JSON["materias"] = {}
        for id_materia in self.materias:
            materia = self.materias[id_materia]
            parametros_JSON["materias"][id_materia] = materia.generar_JSON()

        parametros_JSON["horarios"] = {}
        for id_materia in self.horarios:
            horarios = []
            for curso in self.horarios[id_materia]:
                horarios.append(curso.generar_JSON())
            parametros_JSON["horarios"][id_materia] = horarios

        parametros_JSON["creditos_minimos_electivas"] = self.creditos_minimos_electivas

        parametros_JSON["nombre_archivo_pulp"] = self.nombre_archivo_pulp
        parametros_JSON["nombre_archivo_resultados_pulp"] = self.nombre_archivo_resultados_pulp
        parametros_JSON["nombre_archivo_pulp_optimizado"] = self.nombre_archivo_pulp_optimizado

        parametros_JSON["franja_minima"] = self.franja_minima
        parametros_JSON["franja_maxima"] = self.franja_maxima
        parametros_JSON["dias"] = self.dias

        parametros_JSON["max_cuatrimestres"] = self.max_cuatrimestres
        parametros_JSON["max_cant_materias_por_cuatrimestre"] = self.max_cant_materias_por_cuatrimestre

        parametros_JSON["materias_CBC_pendientes"] = self.materias_CBC_pendientes[:]

        parametros_JSON["orientacion"] = self.orientacion
        parametros_JSON["id_carrera"] = self.id_carrera

        parametros_JSON["cuatrimestre_minimo_para_materia"] = dict(self.cuatrimestre_minimo_para_materia)
        parametros_JSON["creditos_minimos_tematicas"] = dict(self.creditos_minimos_tematicas)

        parametros_JSON["cuatrimestre_inicio"] = self.cuatrimestre_inicio
        parametros_JSON["anio_inicio"] = self.anio_inicio

        parametros_JSON["materias_incompatibles"] = dict(self.materias_incompatibles)

        parametros_JSON["max_horas_cursada"] = self.max_horas_cursada
        parametros_JSON["max_horas_extras"] = self.max_horas_extras

        parametros_JSON["materia_trabajo_final"] = []
        for materia in self.materia_trabajo_final:
            parametros_JSON["materia_trabajo_final"].append(materia.generar_JSON())

        parametros_JSON["plan_generado"] = []
        for cuatrimestre_plan in self.plan_generado:
            cuatrimeste = {}
            for id_materia in cuatrimestre_plan:
                cuatrimeste[id_materia] = cuatrimestre_plan[id_materia]
            parametros_JSON["plan_generado"].append(cuatrimeste)

        parametros_JSON["id_plan_estudios"] = self.id_plan_estudios
        parametros_JSON["estado_plan_de_estudios"] = self.estado_plan_de_estudios

        parametros_JSON["user_id"] = self.user_id

        parametros_JSON["creditos_preacumulados"] = self.creditos_preacumulados
        parametros_JSON["hash_precalculado"] = self.hash_precalculado

        return parametros_JSON


    def set_franjas(self, minima, maxima):
        self.franja_minima = minima
        self.franja_maxima = maxima

    def quitar_materia_por_id(self, id_materia, actualizar_creditos=False):
        if not id_materia in self.materias:
            return

        materia = self.materias.pop(id_materia)
        if materia.tipo == ELECTIVA and actualizar_creditos and self.creditos_minimos_electivas > 0:
            self.creditos_minimos_electivas -= materia.creditos
            if self.creditos_minimos_electivas < 0:
                self.creditos_minimos_electivas = 0

        if actualizar_creditos:
            self.creditos_preacumulados += materia.creditos

        correlativas_plan = self.plan[id_materia] if id_materia in self.plan else []
        for id_materia_que_la_tiene_de_correlativa in correlativas_plan:
            if not id_materia_que_la_tiene_de_correlativa in self.materias:
                continue
            materia_actual = self.materias[id_materia_que_la_tiene_de_correlativa]
            if id_materia in materia_actual.correlativas:
                materia_actual.correlativas.remove(id_materia)

        for id_correlativa in materia.correlativas:
            if not id_correlativa in self.plan or not materia.id_materia in self.plan[id_correlativa]:
                continue
            self.plan[id_correlativa].remove(materia.id_materia)

        if id_materia in self.plan:
            del (self.plan[id_materia])

        if id_materia in self.horarios:
            del (self.horarios[id_materia])

    def plan_esta_finalizado(self):
        electivas_completas = self.creditos_en_electivas_estan_completos()

        hay_obligatorias_pendientes = False
        for id_materia in list(self.plan.keys()):
            if not id_materia in self.materias:
                continue

            materia = self.materias[id_materia]
            if materia.tipo == OBLIGATORIA:
                hay_obligatorias_pendientes = True
                if not electivas_completas:
                    break
            elif electivas_completas:
                self.quitar_materia_por_id(id_materia, False)

        return not hay_obligatorias_pendientes and electivas_completas and not self.materia_trabajo_final

    def creditos_en_electivas_estan_completos(self):
        return (self.creditos_minimos_electivas == 0 and not self.creditos_minimos_tematicas)

