
# pip install matplotlib
# sudo apt install python3-tk
import matplotlib.pyplot as plt

TOTAL_CUATRIMESTRES_PLAN = 0
SEGUNDOS = 1
TOTAL_MATERIAS_DISPONIBLES = 2
TOTAL_CURSOS_DISPONIBLES = 3
MAX_MATERIAS_POR_CUATRIMESTRE = 4
ALGORITMO = 5

TUPLA_MAT_DISPONIBLES = 0
TUPLA_TOTAL_CUATRIMESTRES = 1
TUPLA_SEGUNDOS = 2

class DatosAlgoritmo():
    POS_CUATRIMESTRES = 0
    POS_SEGUNDOS = 1

    def __init__(self, nombre):
        self.datos = {}
        self.nombre = nombre

    def convertir_string_decimal(self, texto_numero):
        datos_decimales = texto_numero.split('.')
        numero = int(datos_decimales[0])
        if len(datos_decimales) > 1:
            decimal = datos_decimales[1]
            numero += int(decimal) / (10**len(decimal))
        return numero

    def guardar_datos(self, datos):
        datos_materias = self.datos.get(datos[MAX_MATERIAS_POR_CUATRIMESTRE], {})

        total_materias_disp = int(datos[TOTAL_MATERIAS_DISPONIBLES])
        segundos = self.convertir_string_decimal(datos[SEGUNDOS])
        total_cuatrimestres = int(datos[TOTAL_CUATRIMESTRES_PLAN])

        listas_datos = datos_materias.get(total_materias_disp, ([],[]))
        listas_datos[self.POS_CUATRIMESTRES].append(total_cuatrimestres)
        listas_datos[self.POS_SEGUNDOS].append(segundos)

        datos_materias[total_materias_disp] = listas_datos
        self.datos[datos[MAX_MATERIAS_POR_CUATRIMESTRE]] = datos_materias

    def ordenar_y_generar_tuplas(self):
        for cantidad_max_materias_por_cuatrimestre in self.datos:
            self.datos[cantidad_max_materias_por_cuatrimestre] = sorted(
                self._diccionario_a_lista_con_tuplas(self.datos[cantidad_max_materias_por_cuatrimestre]),
                key=lambda tupla: tupla[TUPLA_MAT_DISPONIBLES]
            )

    def _diccionario_a_lista_con_tuplas(self, diccionario_datos):
        nueva_lista = []
        for total_materias_disp in diccionario_datos:
            datos_actuales = diccionario_datos[total_materias_disp]

            #Promedio
            l_cuatrimestres = datos_actuales[self.POS_CUATRIMESTRES]
            total_cuatrimestres = sum(l_cuatrimestres) / len(l_cuatrimestres)

            #Promedio
            l_segundos = datos_actuales[self.POS_SEGUNDOS]
            segundos = sum(l_segundos) / len(l_segundos)

            nueva_lista.append((total_materias_disp, total_cuatrimestres, segundos))

        return nueva_lista


def cargar_datos(ruta, PLE, Greedy):
    with open(ruta, 'r') as f:
        primera = True
        for linea in f:
            if primera:
                primera = False
                continue

            linea = linea.rstrip("\n")
            datos = linea.split(",")

            if datos[ALGORITMO] == "PLE":
                PLE.guardar_datos(datos)
            else:
                Greedy.guardar_datos(datos)

def mostrar_grafico(ylabel='Tiempo [Segundos]'):
    plt.legend()
    plt.grid()
    plt.xlabel('Cantidad de Materias Disponibles')
    plt.ylabel(ylabel)
    plt.show()

def graficar_mismo_algoritmo_con_cada_linea_cantidad_maxima_materias_diferente(algoritmo):
    plt.title('Tiempo algoritmo {} respecto de la máx. cant. de materias por cuatrimestre'.format(algoritmo.nombre))
    
    for cantidad_max_materias_por_cuatrimestre in algoritmo.datos:
        datos_x, datos_y = generar_datos_x_e_y_algoritmo(algoritmo.datos[cantidad_max_materias_por_cuatrimestre])
        label_linea = 'Max materias = {}'.format(cantidad_max_materias_por_cuatrimestre)
        plt.plot(datos_x, datos_y, label=label_linea)
    mostrar_grafico()

def generar_datos_x_e_y_algoritmo(datos_algoritmo, pos_dato=TUPLA_SEGUNDOS):
    datos_x = []
    datos_y = []
    for tupla in datos_algoritmo:
        datos_x.append(tupla[TUPLA_MAT_DISPONIBLES])
        datos_y.append(tupla[pos_dato])
    return datos_x, datos_y

def generar_grafico_algoritmos_combinados_segundos_para_cada_cantidad_maxima_de_materias_por_cuatrimestre(algoritmos):    
    vs_algoritmos = ""
    VERSUS = " vs. "
    for algoritmo in algoritmos:
        vs_algoritmos += algoritmo.nombre + VERSUS
    vs_algoritmos = vs_algoritmos[:len(vs_algoritmos)-len(VERSUS)]

    for cantidad_max_materias_por_cuatrimestre in algoritmos[0].datos: #Todos deben tener las mismas combinaciones
        plt.title('{} - Máx. cant. de materias por cuatrimestre: {}'.format(vs_algoritmos, cantidad_max_materias_por_cuatrimestre))
        for algoritmo in algoritmos:
            datos_x, datos_y = generar_datos_x_e_y_algoritmo(algoritmo.datos[cantidad_max_materias_por_cuatrimestre])    
            plt.plot(datos_x, datos_y, label='Algoritmo {}'.format(algoritmo.nombre))
        mostrar_grafico()

def generar_grafico_algoritmos_combinados_total_cuatrimestres_para_cada_cantidad_maxima_de_materias_por_cuatrimestre(algoritmos):    
    vs_algoritmos = ""
    VERSUS = " vs. "
    for algoritmo in algoritmos:
        vs_algoritmos += algoritmo.nombre + VERSUS
    vs_algoritmos = vs_algoritmos[:len(vs_algoritmos)-len(VERSUS)]

    for cantidad_max_materias_por_cuatrimestre in algoritmos[0].datos: #Todos deben tener las mismas combinaciones
        plt.title('{} - Máx. cant. de materias por cuatrimestre: {}'.format(vs_algoritmos, cantidad_max_materias_por_cuatrimestre))
        for algoritmo in algoritmos:
            datos_x, datos_y = generar_datos_x_e_y_algoritmo(algoritmo.datos[cantidad_max_materias_por_cuatrimestre], TUPLA_TOTAL_CUATRIMESTRES)    
            plt.plot(datos_x, datos_y, label='Algoritmo {}'.format(algoritmo.nombre))
        mostrar_grafico('Total de cuatrimestres')

def convertir_tiempo(tiempo):
    minutos = tiempo // 60
    segundos = tiempo - minutos * 60
    horas = minutos // 60
    minutos = minutos - horas * 60

    msj = ""
    if horas > 0:
        msj += "{} horas, ".format(horas)

    if minutos > 0:
        texto_minutos =  "minutos" if minutos > 1 else "minuto"
        msj += "{} {}, ".format(minutos, texto_minutos)

    msj += "{0:.2f} segundos".format(segundos)
    return msj    

def imprimir_resultados_tiempo_maximo_algoritmo(algoritmo):
    tiempo_maximo = 0
    datos_maximo = []

    for cantidad_max_materias_por_cuatrimestre in algoritmo.datos:
        for tupla in algoritmo.datos[cantidad_max_materias_por_cuatrimestre]:
            if tupla[TUPLA_SEGUNDOS] == tiempo_maximo:
                datos_a_guardar = tupla + (cantidad_max_materias_por_cuatrimestre,)
                datos_maximo.append(tupla)
            elif tupla[TUPLA_SEGUNDOS] > tiempo_maximo:
                tiempo_maximo = tupla[TUPLA_SEGUNDOS]
                datos_a_guardar = tupla + (cantidad_max_materias_por_cuatrimestre,)
                datos_maximo = [datos_a_guardar]

    print()
    print("El tiempo maximo registrado para el algoritmo {} se dio para:".format(algoritmo.nombre))
    for tupla in datos_maximo:
        print("--------------------------")
        print("Tiempo: {}".format(convertir_tiempo(tupla[TUPLA_SEGUNDOS])))
        print("Cantidad de materias Disponibles: {}".format(tupla[TUPLA_MAT_DISPONIBLES]))
        print("Max cantidad de materias por cuatrimestre: {}".format(tupla[-1]))
        print("Total cuatrimestres: {}".format(tupla[TUPLA_TOTAL_CUATRIMESTRES]))

def generar_graficos_por_maquina(archivo, texto_maquina):
    PLE = DatosAlgoritmo('PLE ({})'.format(texto_maquina))
    Greedy = DatosAlgoritmo('Greedy ({})'.format(texto_maquina))       
    cargar_datos(archivo, PLE, Greedy)

    PLE.ordenar_y_generar_tuplas()
    Greedy.ordenar_y_generar_tuplas()

    imprimir_resultados_tiempo_maximo_algoritmo(PLE)
    imprimir_resultados_tiempo_maximo_algoritmo(Greedy)
    
    graficar_mismo_algoritmo_con_cada_linea_cantidad_maxima_materias_diferente(Greedy)
    graficar_mismo_algoritmo_con_cada_linea_cantidad_maxima_materias_diferente(PLE)

    generar_grafico_algoritmos_combinados_segundos_para_cada_cantidad_maxima_de_materias_por_cuatrimestre([PLE, Greedy])
    generar_grafico_algoritmos_combinados_total_cuatrimestres_para_cada_cantidad_maxima_de_materias_por_cuatrimestre([PLE, Greedy])

    return PLE, Greedy

def generar_graficos_estadisticas():
    PLE_maq1, Greedy_maq1 = generar_graficos_por_maquina('estadisticas_algoritmos_maq1.csv', 'M1')
    PLE_maq2, Greedy_maq2 = generar_graficos_por_maquina('estadisticas_algoritmos_maq2.csv', 'M2')

    generar_grafico_algoritmos_combinados_segundos_para_cada_cantidad_maxima_de_materias_por_cuatrimestre([PLE_maq1, PLE_maq2])
    generar_grafico_algoritmos_combinados_segundos_para_cada_cantidad_maxima_de_materias_por_cuatrimestre([Greedy_maq1, Greedy_maq2])

generar_graficos_estadisticas()
