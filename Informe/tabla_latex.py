ENTER = "\n"

TOTAL_CUATRIMESTRES = 0
SEGUNDOS = 1
MATERIAS_DISPONIBLES = 2
CURSOS_DISPONIBLES = 3
MAX_CANT_MATERIAS_POR_CUATRIMESTRE = 4
ALGORITMO = 5

def convertir_tiempo(tiempo):
    minutos = tiempo // 60
    segundos = tiempo - minutos * 60
    horas = minutos // 60
    minutos = minutos - horas * 60

    msj = ""
    if horas > 0:
        msj += "{} hs, ".format(horas)

    if minutos > 0:
        msj += "{} min, ".format(minutos)

    msj += "{0:.2f} seg".format(segundos)
    return msj    


def agregar_titulos(arch):
    arch.write("\\begin{longtable}{| c | c | c | c |}" + ENTER)
    arch.write("\\hline" + ENTER)

    arch.write("Total   & Tiempo de & Cantidad de & Max. materias  \\\\" + ENTER)
    arch.write("cuatrimestres &  generación &  Materias disponibles & por cuatrimestre \\\\" + ENTER)
    arch.write("\\hline \\hline" + ENTER)
    arch.write("\\endfirsthead" + ENTER)

    arch.write("\\hline" + ENTER)
    arch.write("Total   & Tiempo de & Cantidad de & Max. materias  \\\\" + ENTER)
    arch.write("cuatrimestres &  generación &  Materias disponibles & por cuatrimestre \\\\" + ENTER)
    arch.write("\\hline \\hline" + ENTER)
    arch.write("\\endhead" + ENTER)

    arch.write("\\endfoot" + ENTER)
    arch.write("\\endlastfoot" + ENTER)


def finalizar_tabla(arch, tipo_algoritmo, numero_maquina):
    titulo_tabla = "Ejecucion algoritmo {} ({})".format(tipo_algoritmo, numero_maquina)
    arch.write("\caption{" + titulo_tabla + "}" + ENTER)
    arch.write("\\end{longtable}" + ENTER)


def escribir_linea_tabla(datos, arch):
    texto = ""
    texto += datos[TOTAL_CUATRIMESTRES] + " & "
    texto += convertir_tiempo(float(datos[SEGUNDOS])) + " & "
    texto += datos[MATERIAS_DISPONIBLES] + " & "
    texto += datos[MAX_CANT_MATERIAS_POR_CUATRIMESTRE]
    texto += "\\\\"

    arch.write(texto + ENTER)
    arch.write("\\hline" + ENTER)


def cargar_datos(ruta, arch, tipo_algoritmo):
    with open(ruta, 'r') as f:
        primera = True
        for linea in f:
            if primera:
                primera = False
                continue

            linea = linea.rstrip("\n")
            datos = linea.split(",")

            if datos[ALGORITMO] == tipo_algoritmo:
                escribir_linea_tabla(datos, arch)


def generar_archivo_con_datos_algoritmo(ruta_estadisticas, ruta_tabla, tipo_algoritmo, numero_maquina):
    with open(ruta_tabla, 'w') as arch:
        agregar_titulos(arch)
        cargar_datos(ruta_estadisticas, arch, tipo_algoritmo)        
        finalizar_tabla(arch, tipo_algoritmo, numero_maquina)

def generar_archivos_tabla_latex(ruta_estadisticas, ruta_tabla_Greedy, ruta_tabla_PLE, numero_maquina):
    generar_archivo_con_datos_algoritmo(ruta_estadisticas, ruta_tabla_Greedy, 'GREEDY', numero_maquina)
    generar_archivo_con_datos_algoritmo(ruta_estadisticas, ruta_tabla_PLE, 'PLE', numero_maquina)

generar_archivos_tabla_latex('estadisticas_algoritmos_maq1.csv', 'tabla_latex_Greedy_m1.txt', 'tabla_latex_PLE_m1.txt', 'M1')
generar_archivos_tabla_latex('estadisticas_algoritmos_maq2.csv', 'tabla_latex_Greedy_m2.txt', 'tabla_latex_PLE_m2.txt', 'M2')
