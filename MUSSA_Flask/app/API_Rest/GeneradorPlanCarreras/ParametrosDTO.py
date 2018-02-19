from app.API_Rest.GeneradorPlanCarreras.Constantes import *
from app.utils import cmp_to_key

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

        # Nuevos parametros a agregar

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

    def set_franjas(self, minima, maxima):
        self.franja_minima = minima
        self.franja_maxima = maxima

    def quitar_materia_por_codigo(self, codigo, actualizar_creditos=False):
        if not codigo in self.materias:
            return

        materia = self.materias.pop(codigo)
        if materia.tipo == ELECTIVA and actualizar_creditos and self.creditos_minimos_electivas > 0:
            self.creditos_minimos_electivas -= materia.creditos
            if self.creditos_minimos_electivas < 0:
                self.creditos_minimos_electivas = 0

        correlativas_plan = self.plan[codigo] if codigo in self.plan else []
        for cod_materia_que_la_tiene_de_correlativa in correlativas_plan:
            if not cod_materia_que_la_tiene_de_correlativa in self.materias:
                continue
            materia_actual = self.materias[cod_materia_que_la_tiene_de_correlativa]
            if codigo in materia_actual.correlativas:
                materia_actual.correlativas.remove(codigo)

        if codigo in self.plan:
            del (self.plan[codigo])

    def plan_esta_finalizado(self):
        electivas_completas = self.creditos_en_electivas_estan_completos()

        hay_obligatorias_pendientes = False
        for cod_materia in list(self.plan.keys()):
            if not cod_materia in self.materias:
                continue

            materia = self.materias[cod_materia]
            if materia.tipo == OBLIGATORIA:
                hay_obligatorias_pendientes = True
                if not electivas_completas:
                    break
            elif electivas_completas:
                self.quitar_materia_por_codigo(cod_materia, False)

        return not hay_obligatorias_pendientes and electivas_completas and not self.materia_trabajo_final

    def creditos_en_electivas_estan_completos(self):
        return (self.creditos_minimos_electivas == 0 and not self.creditos_minimos_tematicas)

    def generar_lista_franjas_limpia(self):
        franjas_por_dia = {}
        for dia in self.dias:
            franjas = [False for i in range(self.franja_minima, self.franja_maxima + 1)]
            franjas_por_dia[dia] = franjas
        return franjas_por_dia

    def obtener_materias_disponibles(self, creditos_actuales):
        disponibles_obligatorias = []
        disponibles_electivas_prioritarias = []
        disponibles_electivas_secundarias = []

        for cod_materia in self.plan:
            materia = self.materias[cod_materia]
            if not materia.correlativas and materia.creditos_minimos_aprobados <= creditos_actuales:
                for curso in self.horarios[cod_materia]:
                    self.agregar_materia_al_listado_correspondiente(materia, curso, disponibles_obligatorias,
                                                                    disponibles_electivas_prioritarias,
                                                                    disponibles_electivas_secundarias)

        disponibles_obligatorias = sorted(disponibles_obligatorias, key=cmp_to_key(self.cmp_materias_obligatorias))

        disponibles_electivas_prioritarias = sorted(
            disponibles_electivas_prioritarias,
            key=cmp_to_key(self.cmp_materias_electivas)
        )

        disponibles_electivas_secundarias = sorted(
            disponibles_electivas_secundarias,
            key=cmp_to_key(self.cmp_materias_electivas)
        )

        disponibles = self.concatenar_listas_por_horarios(disponibles_obligatorias,
                                                          disponibles_electivas_prioritarias)

        self.concatenar_materias_trabajo_final(disponibles, creditos_actuales)

        # Concateno al final todas las electivas que no aportan creditos para las tematicas
        for materia_electiva in disponibles_electivas_secundarias:
            disponibles.append(materia_electiva)

        return disponibles

    def se_encuentra_materia_en_plan_generado(self, cod_materia, materias_cuatrimestre_actual):
        for cuatrimestre in self.plan_generado:
            if cod_materia in cuatrimestre:
                return True
        return cod_materia in materias_cuatrimestre_actual

    def concatenar_materias_trabajo_final(self, disponibles, creditos_actuales):
        # Luego de las materias electivas que aportan creditos de tematicas y obligatorias, si están habilitadas
        # concateno las dos partes del trabajo final (tesis o tp si corresponde)
        for materia_tp in self.materia_trabajo_final:
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

    def concatenar_listas_por_horarios(self, obligatorias, electivas):
        """
        Devuelve una nueva lista con la concatenación de las materias obligatorias
        y electivas comparandolas por el horario de finalización.
        """
        disponibles = []

        obligatoria = obligatorias.pop(0) if obligatorias else None
        electiva = electivas.pop(0) if electivas else None
        while (obligatoria and electiva):
            materia_obligatoria, curso_obligatorio = obligatoria
            materia_electiva, curso_electiva = electiva

            if self.cmp_horario_finalizacion_curso(curso_obligatorio, curso_electiva) == self.CMP_SEGUNDO_ES_MENOR:
                disponibles.append(electiva)
                electiva = electivas.pop(0) if electivas else None
            else:
                disponibles.append(obligatoria)
                obligatoria = obligatorias.pop(0) if obligatorias else None

        for obligatoria in obligatorias:
            disponibles.append(obligatoria)

        for electiva in electivas:
            disponibles.append(electiva)

        return disponibles

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

        correlativas_liberadas_a = self.plan[materia_a.codigo]
        correlativas_liberadas_b = self.plan[materia_b.codigo]

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

        if curso_a.puntaje > curso_b.puntaje:
            return self.CMP_PRIMERO_ES_MENOR

        if curso_a.puntaje < curso_b.puntaje:
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

        correlativas_liberadas_a = self.plan[materia_a.codigo]
        correlativas_liberadas_b = self.plan[materia_b.codigo]

        if correlativas_liberadas_a > correlativas_liberadas_b:
            return self.CMP_PRIMERO_ES_MENOR

        if correlativas_liberadas_a < correlativas_liberadas_b:
            return self.CMP_SEGUNDO_ES_MENOR

        if curso_a.puntaje > curso_b.puntaje:
            return self.CMP_PRIMERO_ES_MENOR

        if curso_a.puntaje < curso_b.puntaje:
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
