from app.API_Rest.GeneradorPlanCarreras.Constantes import *

MENOR_IGUAL = 0
MAYOR_IGUAL = 1

def obtener_variables_candidatas(parametros):
    variables_candidatas = {}
    with open(parametros.nombre_archivo_pulp, 'r') as arch:
        for linea in arch:
            linea = linea.rstrip('\n')
            ecuacion = linea.split("prob += (")
            if len(ecuacion) < 2: #No es la linea buscada
                continue
            menor_igual = ecuacion[1].split(" <= 0")
            mayor_igual = ecuacion[1].split(" >= 0")
            
            variable_actual = menor_igual[0] #o mayor igual, es equivalente
            acumulados = variables_candidatas.get(variable_actual, [0,0])
            acumulados[MENOR_IGUAL] += 1 if len(menor_igual) == 2 else 0
            acumulados[MAYOR_IGUAL] += 1 if len(menor_igual) == 2 else 0
            variables_candidatas[variable_actual] = acumulados

    return variables_candidatas


def obtener_variables_a_eliminar(parametros):
    variables_candidatas = obtener_variables_candidatas(parametros)

    variables_a_eliminar = []
    for candidata in variables_candidatas:

        multiples_variables = candidata.split()
        if len(multiples_variables) > 1: #Solo me sirve si es una unica variable
            continue

        acumulados = variables_candidatas[candidata]
        if acumulados[MENOR_IGUAL] == acumulados[MAYOR_IGUAL] == 1:
            variables_a_eliminar.append(candidata)

    return variables_a_eliminar


def reemplazar_todas_las_apariciones(texto, valor_a_reeemplazar, nuevo_valor):
    anterior = ""
    while (anterior != texto):
        anterior = texto
        texto = texto.replace(valor_a_reeemplazar, nuevo_valor)
    return texto


def define_variable_mayor_a_cero(linea):
    inicio = "prob += ("
    final = " >= 0)"
    
    linea_aux = linea[len(inicio):]

    if final in linea_aux:
        linea_aux = linea_aux.replace(final, "")
        variable_mayor_a_cero = linea_aux.split()

        if len(variable_mayor_a_cero) == 1:
            return True

    return False


def define_variable_menor_a_infinito(linea):
    inicio = "prob += ("
    final = " <= 0 + (1 - 0) * {})".format(INFINITO)
    
    linea_aux = linea[len(inicio):]

    if final in linea_aux:
        linea_aux = linea_aux.replace(final, "")
        variable_menor_a_infinito = linea_aux.split()

        if len(variable_menor_a_infinito) == 1:
            return True

    return False


def reemplazar_productos_franjas_por_cero(parametros, linea):
    for franja in range(parametros.franja_minima, parametros.franja_maxima +1):
        producto = " {} * 0".format(franja)
        linea = reemplazar_todas_las_apariciones(linea, producto, " 0")
    return linea


def limpiar_linea(parametros, linea, variables_a_eliminar):
    for variable in variables_a_eliminar:
        if variable not in linea:
            continue

        if "LpVariable" in linea:
            return "" #La linea no se escribe, no es necesario revisar las demas variables

        if "arch.write" in linea:
            return """    arch.write("{};0" + '\\n')\n""".format(variable)
            
        linea = reemplazar_todas_las_apariciones(linea, variable, "0")

        linea = reemplazar_apariciones_suma_cero(linea)

        linea = reemplazar_productos_franjas_por_cero(parametros, linea)

        linea = reemplazar_apariciones_suma_cero(linea)

    return linea


def reemplazar_apariciones_suma_cero(linea):
    linea = reemplazar_todas_las_apariciones(linea, "+ 0 ", "")
    linea = reemplazar_todas_las_apariciones(linea, "- 0 ", "")
    linea = reemplazar_todas_las_apariciones(linea, " 0 + 0 ", "0")
    linea = reemplazar_todas_las_apariciones(linea, "(0 + 0)", "0")
    linea = reemplazar_todas_las_apariciones(linea, " 0 + 0)", "0)")

    return linea


def limpiar_archivo(parametros, variables_a_eliminar, arch, arch_optimizado):
    for linea in arch:

        linea = limpiar_linea(parametros, linea, variables_a_eliminar)

        if not linea:
            continue

        if linea == "prob += (0 <= 0)\n" or linea == "prob += (0 >= 0)\n":
            continue #Es una tautologia, no hace falta escribirla

        if define_variable_mayor_a_cero(linea):
            continue  #Todas las variables de este problema son mayores o iguales que 0

        if define_variable_menor_a_infinito(linea):
            continue #Todas las variables son menores a infinito, es una ecuacion anulable

        arch_optimizado.write(linea)


def guardar_archivo_optimizado(parametros, variables_a_eliminar):
    with open(parametros.nombre_archivo_pulp, 'r') as arch:
        with open(parametros.nombre_archivo_pulp_optimizado, 'w') as arch_optimizado:
            limpiar_archivo(parametros, variables_a_eliminar, arch, arch_optimizado)


def optimizar_codigo_pulp(parametros):
    variables_a_eliminar = obtener_variables_a_eliminar(parametros)
    guardar_archivo_optimizado(parametros, variables_a_eliminar)
