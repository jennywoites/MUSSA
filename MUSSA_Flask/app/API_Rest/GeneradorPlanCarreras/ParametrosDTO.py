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

    def copia_profunda(self):
        copia_parametros = Parametros()

        copia_parametros.primer_cuatrimestre_es_impar = self.primer_cuatrimestre_es_impar

        copia_parametros.plan = {}
        for id_materia in self.plan:
            copia_parametros.plan[id_materia] = self.plan[id_materia][:]

        copia_parametros.materias = {}
        for id_materia in self.materias:
            copia_parametros.materias[id_materia] = self.materias[id_materia].copia_profunda()

        copia_parametros.horarios = {}
        for id_materia in self.horarios:
            copia_parametros.horarios[id_materia] = self.horarios[id_materia][:]

        copia_parametros.horarios_no_permitidos = self.horarios_no_permitidos[:]
        copia_parametros.creditos_minimos_electivas = self.creditos_minimos_electivas
        copia_parametros.nombre_archivo_pulp = self.nombre_archivo_pulp
        copia_parametros.nombre_archivo_resultados_pulp = self.nombre_archivo_resultados_pulp
        copia_parametros.nombre_archivo_pulp_optimizado = self.nombre_archivo_pulp_optimizado
        copia_parametros.franja_minima = self.franja_minima
        copia_parametros.franja_maxima = self.franja_maxima
        copia_parametros.dias = self.dias
        copia_parametros.max_cuatrimestres = self.max_cuatrimestres
        copia_parametros.max_cant_materias_por_cuatrimestre = self.max_cant_materias_por_cuatrimestre

        copia_parametros.materias_CBC_pendientes = self.materias_CBC_pendientes[:]

        copia_parametros.orientacion = self.orientacion
        copia_parametros.id_carrera = self.id_carrera

        copia_parametros.cuatrimestre_minimo_para_materia = {}
        for id_materia in self.cuatrimestre_minimo_para_materia:
            copia_parametros.cuatrimestre_minimo_para_materia[id_materia] = self.cuatrimestre_minimo_para_materia[
                id_materia]

        copia_parametros.creditos_minimos_tematicas = {}
        for tematica in self.creditos_minimos_tematicas:
            copia_parametros.creditos_minimos_tematicas[tematica] = self.creditos_minimos_tematicas[tematica]

        copia_parametros.cuatrimestre_inicio = self.cuatrimestre_inicio
        copia_parametros.anio_inicio = self.anio_inicio

        copia_parametros.materias_incompatibles = {}
        for id_materia in self.materias_incompatibles:
            copia_parametros.materias_incompatibles[id_materia] = self.materias_incompatibles[id_materia][:]

        copia_parametros.max_horas_cursada = self.max_horas_cursada
        copia_parametros.max_horas_extras = self.max_horas_extras

        copia_parametros.materia_trabajo_final = []
        for materia in self.materia_trabajo_final:
            copia_parametros.materia_trabajo_final.append(materia.copia_profunda())

        copia_parametros.plan_generado = []
        for cuatrimestre in self.plan_generado:
            copia_materias_cuatrimestre = {}
            for id_materia in cuatrimestre:
                copia_materias_cuatrimestre[id_materia] = cuatrimestre[id_materia]
            copia_parametros.plan_generado.append(copia_materias_cuatrimestre)

        copia_parametros.id_plan_estudios = self.id_plan_estudios
        copia_parametros.estado_plan_de_estudios = self.estado_plan_de_estudios

        copia_parametros.user_id = self.user_id

        copia_parametros.creditos_preacumulados = self.creditos_preacumulados
        copia_parametros.hash_precalculado = self.hash_precalculado

        return copia_parametros

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

    def generar_lista_franjas_limpia(self):
        franjas_por_dia = {}
        for dia in self.dias:
            # Por mas que haya una franja minima se accede por el valor directo de la franja - 1
            # asi que es necesario generar todos los espacios
            franjas = [False for i in range(1, self.franja_maxima + 1)]
            franjas_por_dia[dia] = franjas
        return franjas_por_dia

    def obtener_materias_disponibles(self, creditos_actuales, ultimo_cuatrimestre_generado):
        cuatrimestre_actual = ultimo_cuatrimestre_generado + 1

        disponibles_obligatorias = []
        disponibles_electivas_prioritarias = []
        disponibles_electivas_secundarias = []

        for id_materia in self.plan:
            materia = self.materias[id_materia]

            if self.la_materia_esta_habilitada(materia, creditos_actuales):
                for curso in self.horarios[id_materia]:
                    if not self.curso_esta_habilitado_en_el_cuatrimestre(curso, cuatrimestre_actual):
                        continue

                    self.agregar_materia_al_listado_correspondiente(materia, curso, disponibles_obligatorias,
                                                                    disponibles_electivas_prioritarias,
                                                                    disponibles_electivas_secundarias)

        disponibles = sorted(disponibles_obligatorias, key=cmp_to_key(self.cmp_materias_obligatorias))

        disponibles_electivas_prioritarias = sorted(
            disponibles_electivas_prioritarias,
            key=cmp_to_key(self.cmp_materias_electivas)
        )

        for materia_electiva in disponibles_electivas_prioritarias:
            disponibles.append(materia_electiva)

        self.concatenar_materias_trabajo_final(disponibles, creditos_actuales)

        disponibles_electivas_secundarias = sorted(
            disponibles_electivas_secundarias,
            key=cmp_to_key(self.cmp_materias_electivas)
        )

        # Concateno al final todas las electivas que no aportan creditos para las tematicas
        for materia_electiva in disponibles_electivas_secundarias:
            disponibles.append(materia_electiva)

        return disponibles

    def curso_esta_habilitado_en_el_cuatrimestre(self, curso, cuatrimestre_actual):
        es_par = (cuatrimestre_actual % 2 == 0)
        return (curso.se_dicta_segundo_cuatrimestre
                if self.primer_cuatrimestre_es_impar else curso.se_dicta_primer_cuatrimestre) if es_par \
            else (curso.se_dicta_primer_cuatrimestre if self.primer_cuatrimestre_es_impar else
                  curso.se_dicta_segundo_cuatrimestre)

    def la_materia_esta_habilitada(self, materia, creditos_actuales):
        return (not materia.correlativas and
                materia.creditos_minimos_aprobados <= creditos_actuales and
                self.tiene_cuatrimestre_minimo_cumplido(materia.id_materia))

    def tiene_cuatrimestre_minimo_cumplido(self, id_materia):
        if not id_materia in self.cuatrimestre_minimo_para_materia:
            return True

        return self.cuatrimestre_minimo_para_materia[id_materia] <= len(self.plan_generado)

    def se_encuentra_materia_en_plan_generado(self, id_materia, materias_cuatrimestre_actual):
        for cuatrimestre in self.plan_generado:
            if id_materia in cuatrimestre:
                return True
        return id_materia in materias_cuatrimestre_actual

    def concatenar_materias_trabajo_final(self, disponibles, creditos_actuales):
        # Luego de las materias electivas que aportan creditos de tematicas y obligatorias, si están habilitadas
        # concateno la primer parte disponible del trabajo final (tesis o tp si corresponde)
        if self.materia_trabajo_final:
            materia_tp = self.materia_trabajo_final[0]
            if not materia_tp.correlativas and materia_tp.creditos_minimos_aprobados <= creditos_actuales:
                disponibles.append((materia_tp, None))

    def agregar_materia_al_listado_correspondiente(self, materia, curso, disponibles_obligatorias,
                                                   disponibles_electivas_prioritarias,
                                                   disponibles_electivas_secundarias):
        if materia.tipo == OBLIGATORIA:
            disponibles_obligatorias.append((materia, curso))
            return

        if not self.creditos_minimos_tematicas:
            disponibles_electivas_prioritarias.append((materia, curso))
            return

        creditos_aportados = self.calcular_creditos_aportados_tematicas(materia)
        if creditos_aportados > 0:
            disponibles_electivas_prioritarias.append((materia, curso))
        else:
            disponibles_electivas_secundarias.append((materia, curso))

    def concatenar_materias_restantes(self, materia_restante, materias, disponibles):
        if materia_restante:
            disponibles.append(materia_restante)

        for materia in materias:
            disponibles.append(materia)

    CMP_PRIMERO_ES_MENOR = -1
    CMP_SON_IGUALES = 0
    CMP_SEGUNDO_ES_MENOR = 1

    def cmp_horario_finalizacion_curso(self, curso_a, curso_b):
        """
        Para definir cual termina antes que otro, ya que cada curso puede tener horarios
        en diferentes dias o más de un horario por dia, se definirá de la siguiente forma:
        La máxima franja de un curso en todos sus dias de cursada comparada con la máxima
        del otro. Por ejemplo si el curso A se cursa Lunes en las franjas 1 a 15 y Viernes
        en las franjas 3 a 17 su máxima franja será 17. Si el curso B de cursa los sabados
        en las franjas 13 a 18, su máxima franja será 18. En este caso el curso A es menor
        que el curso B, aunque A tenga curso varios dias.
        Si ambos tuviesen la misma franja máxima, entonces un curso será menor que otro si
        se cursa menos días. Por ejemplo, si A y B hubiesen tenido la misma franja máxima,
        B hubiese sido menor que A ya que se cursa un solo día.
        Si cursan la misma cantidad de dias, entonces será menor aquel que para la mayor
        cantidad de dias tenga menor horario de finalización.
        Sino, serán iguales.
        """
        franja_maxima_a, cantidad_de_dias_a = self.obtener_franja_maxima_curso_y_cantidad_de_dias_cursada(curso_a)
        franja_maxima_b, cantidad_de_dias_b = self.obtener_franja_maxima_curso_y_cantidad_de_dias_cursada(curso_b)

        if franja_maxima_a < franja_maxima_b:
            return self.CMP_PRIMERO_ES_MENOR

        if franja_maxima_a > franja_maxima_b:
            return self.CMP_SEGUNDO_ES_MENOR

        if cantidad_de_dias_a < cantidad_de_dias_b:
            return self.CMP_PRIMERO_ES_MENOR

        if cantidad_de_dias_a > cantidad_de_dias_b:
            return self.CMP_SEGUNDO_ES_MENOR

        franjas_a = self.obtener_todas_las_franjas_maximas(curso_a)
        franjas_b = self.obtener_todas_las_franjas_maximas(curso_b)

        cantidad_dias_menores_a = 0
        cantidad_dias_menores_b = 0

        franja_a = franjas_a.pop(0)
        franja_b = franjas_b.pop(0)
        while (franja_a and franja_b):
            if franja_a < franja_b:
                cantidad_dias_menores_a += 1
                franja_a = franjas_a.pop(0) if franjas_a else None
            elif franja_a > franja_b:
                cantidad_dias_menores_b += 1
                franja_b = franjas_b.pop(0) if franjas_b else None
            else:
                franja_a = franjas_a.pop(0) if franjas_a else None
                franja_b = franjas_b.pop(0) if franjas_b else None

        if len(franjas_a) > 0:  # Aun quedan franjas en este dia por lo que B es menor
            return self.CMP_SEGUNDO_ES_MENOR

        if len(franjas_b) > 0:  # Aun quedan franjas en este dia por lo que A es menor
            return self.CMP_PRIMERO_ES_MENOR

        if cantidad_dias_menores_a > cantidad_dias_menores_b:
            return self.CMP_PRIMERO_ES_MENOR

        if cantidad_dias_menores_a < cantidad_dias_menores_b:
            return self.CMP_SEGUNDO_ES_MENOR

        return self.CMP_SON_IGUALES

    def obtener_todas_las_franjas_maximas(self, curso):
        franjas = []
        for horario in curso.horarios:
            franjas.append(horario.get_franjas_utilizadas()[-1])
        franjas.sort()
        return franjas

    def obtener_franja_maxima_curso_y_cantidad_de_dias_cursada(self, curso):
        franja_maxima = 1
        dias = []
        for horario in curso.horarios:
            if horario.dia not in dias:
                dias.append(horario.dia)
            franja_maxima = max(franja_maxima, horario.get_franjas_utilizadas()[-1])

        cantidad_de_dias = len(dias)
        return franja_maxima, cantidad_de_dias

    def obtener_total_franjas_ocupadas_en_todos_los_dias_de_curso(self, curso):
        franjas_totales = 0
        for horario in curso.horarios:
            franjas_totales += len(horario.get_franjas_utilizadas())
        return franjas_totales

    def cmp_materias_obligatorias(self, materia_oblig_a, materia_oblig_b):
        """
        La condición de menor se da en base al siguiente criterio:
        * Menor horario de fin
        * La de mayor cantidad de correlativas que libera
        * Mayor cantidad de franjas ocupadas
        * Mayor puntaje
        * Mayor cantidad de creditos
        * La de menor código de materia
        sino son IGUALES
        """
        materia_a, curso_a = materia_oblig_a
        materia_b, curso_b = materia_oblig_b

        menor_curso = self.cmp_horario_finalizacion_curso(curso_a, curso_b)
        if menor_curso != self.CMP_SON_IGUALES:
            return menor_curso

        correlativas_liberadas_a = self.plan[materia_a.id_materia]
        correlativas_liberadas_b = self.plan[materia_b.id_materia]

        if correlativas_liberadas_a > correlativas_liberadas_b:
            return self.CMP_PRIMERO_ES_MENOR

        if correlativas_liberadas_a < correlativas_liberadas_b:
            return self.CMP_SEGUNDO_ES_MENOR

        franjas_a = self.obtener_total_franjas_ocupadas_en_todos_los_dias_de_curso(curso_a)
        franjas_b = self.obtener_total_franjas_ocupadas_en_todos_los_dias_de_curso(curso_b)

        if franjas_a > franjas_b:
            return self.CMP_PRIMERO_ES_MENOR

        if franjas_a < franjas_b:
            return self.CMP_SEGUNDO_ES_MENOR

        if float(curso_a.puntaje) > float(curso_b.puntaje):
            return self.CMP_PRIMERO_ES_MENOR

        if float(curso_a.puntaje) < float(curso_b.puntaje):
            return self.CMP_SEGUNDO_ES_MENOR

        if materia_a.creditos > materia_b.creditos:
            return self.CMP_PRIMERO_ES_MENOR

        if materia_a.creditos < materia_b.creditos:
            return self.CMP_SEGUNDO_ES_MENOR

        codigo_a = materia_a.codigo
        codigo_b = materia_b.codigo

        if codigo_a < codigo_b:
            return self.CMP_PRIMERO_ES_MENOR

        if codigo_a > codigo_b:
            return self.CMP_SEGUNDO_ES_MENOR

        return self.CMP_SON_IGUALES

    def cmp_materias_electivas(self, materia_elect_a, materia_elect_b):
        """
        La condición de menor se da en base al siguiente criterio:
        * Menor horario de fin
        * Mayor cantidad de creditos tematicas
        * Mayor cantidad de credios
        * Menor cantidad de horas de cursada
        * Mayor cantidad de materias que la tienen de correlativa (cuántas libera)
        * La de mayor puntaje
        * La de menor código de materia
        sino son IGUALES
        """
        materia_a, curso_a = materia_elect_a
        materia_b, curso_b = materia_elect_b

        menor_curso = self.cmp_horario_finalizacion_curso(curso_a, curso_b)
        if menor_curso != self.CMP_SON_IGUALES:
            return menor_curso

        creditos_tematicas_a = self.calcular_creditos_aportados_tematicas(materia_a)
        creditos_tematicas_b = self.calcular_creditos_aportados_tematicas(materia_b)

        if creditos_tematicas_a > creditos_tematicas_b:
            return self.CMP_PRIMERO_ES_MENOR

        if creditos_tematicas_a < creditos_tematicas_b:
            return self.CMP_SEGUNDO_ES_MENOR

        if materia_a.creditos > materia_b.creditos:
            return self.CMP_PRIMERO_ES_MENOR

        if materia_a.creditos < materia_b.creditos:
            return self.CMP_SEGUNDO_ES_MENOR

        franjas_a = self.obtener_total_franjas_ocupadas_en_todos_los_dias_de_curso(curso_a)
        franjas_b = self.obtener_total_franjas_ocupadas_en_todos_los_dias_de_curso(curso_b)

        if franjas_a < franjas_b:
            return self.CMP_PRIMERO_ES_MENOR

        if franjas_a > franjas_b:
            return self.CMP_SEGUNDO_ES_MENOR

        correlativas_liberadas_a = self.plan[materia_a.id_materia]
        correlativas_liberadas_b = self.plan[materia_b.id_materia]

        if correlativas_liberadas_a > correlativas_liberadas_b:
            return self.CMP_PRIMERO_ES_MENOR

        if correlativas_liberadas_a < correlativas_liberadas_b:
            return self.CMP_SEGUNDO_ES_MENOR

        if float(curso_a.puntaje) > float(curso_b.puntaje):
            return self.CMP_PRIMERO_ES_MENOR

        if float(curso_a.puntaje) < float(curso_b.puntaje):
            return self.CMP_SEGUNDO_ES_MENOR

        codigo_a = materia_a.codigo
        codigo_b = materia_b.codigo

        if codigo_a < codigo_b:
            return self.CMP_PRIMERO_ES_MENOR

        if codigo_a > codigo_b:
            return self.CMP_SEGUNDO_ES_MENOR

        return self.CMP_SON_IGUALES

    def calcular_creditos_aportados_tematicas(self, materia):
        """
        Calcula el total de creditos aportados a las tematicas, por ejemplo, si aporta a dos tematicas, se multiplica
        por dos la cantidad de creditos de la materia
        """
        creditos_aportados = 0
        for tematica in materia.tematicas_principales:
            if tematica in self.creditos_minimos_tematicas:
                creditos_aportados += min(materia.creditos, self.creditos_minimos_tematicas[tematica])
        return creditos_aportados

    def actualizar_creditos_tematicas_electivas(self, materia):
        for tematica in materia.tematicas_principales:
            if tematica in self.creditos_minimos_tematicas:
                self.creditos_minimos_tematicas[tematica] -= materia.creditos
                if self.creditos_minimos_tematicas[tematica] <= 0:
                    self.creditos_minimos_tematicas.pop(tematica)

    def actualizar_datos_con_parametros_seleccionados(self, parametros_actuales):
        self.primer_cuatrimestre_es_impar = parametros_actuales.primer_cuatrimestre_es_impar
        self.plan = parametros_actuales.plan
        self.materias = parametros_actuales.materias
        self.horarios = parametros_actuales.horarios
        self.horarios_no_permitidos = parametros_actuales.horarios_no_permitidos
        self.creditos_minimos_electivas = parametros_actuales.creditos_minimos_electivas
        self.nombre_archivo_pulp = parametros_actuales.nombre_archivo_pulp
        self.nombre_archivo_resultados_pulp = parametros_actuales.nombre_archivo_resultados_pulp
        self.nombre_archivo_pulp_optimizado = parametros_actuales.nombre_archivo_pulp_optimizado
        self.franja_minima = parametros_actuales.franja_minima
        self.franja_maxima = parametros_actuales.franja_maxima
        self.dias = parametros_actuales.dias
        self.max_cuatrimestres = parametros_actuales.max_cuatrimestres
        self.max_cant_materias_por_cuatrimestre = parametros_actuales.max_cant_materias_por_cuatrimestre
        self.materias_CBC_pendientes = parametros_actuales.materias_CBC_pendientes
        self.orientacion = parametros_actuales.orientacion
        self.id_carrera = parametros_actuales.id_carrera
        self.cuatrimestre_minimo_para_materia = parametros_actuales.cuatrimestre_minimo_para_materia
        self.creditos_minimos_tematicas = parametros_actuales.creditos_minimos_tematicas
        self.cuatrimestre_inicio = parametros_actuales.cuatrimestre_inicio
        self.anio_inicio = parametros_actuales.anio_inicio
        self.materias_incompatibles = parametros_actuales.materias_incompatibles
        self.max_horas_cursada = parametros_actuales.max_horas_cursada
        self.max_horas_extras = parametros_actuales.max_horas_extras
        self.materia_trabajo_final = parametros_actuales.materia_trabajo_final
        self.plan_generado = parametros_actuales.plan_generado
        self.id_plan_estudios = parametros_actuales.id_plan_estudios
        self.estado_plan_de_estudios = parametros_actuales.estado_plan_de_estudios
        self.user_id = parametros_actuales.user_id
        self.creditos_preacumulados = parametros_actuales.creditos_preacumulados
        self.hash_precalculado = parametros_actuales.hash_precalculado
