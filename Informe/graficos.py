
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
TUPLA_SEGUNDOS = 1

class DatosAlgoritmo():
    def __init__(self, nombre):
        self.datos = {}
        self.nombre = nombre

    def convertir_string_decimal(self, texto_numero):
        datos_decimales = texto_numero.split('.')
        numero = int(datos_decimales[0])
        if len(datos_decimales) > 1:
            numero += int(datos_decimales[1]) / 100
        return numero

    def guardar_datos(self, datos):
        datos_materias = self.datos.get(datos[MAX_MATERIAS_POR_CUATRIMESTRE], [])
        tupla_datos = int(datos[TOTAL_MATERIAS_DISPONIBLES]), self.convertir_string_decimal(datos[SEGUNDOS])
        datos_materias.append(tupla_datos)
        self.datos[datos[MAX_MATERIAS_POR_CUATRIMESTRE]] = datos_materias

    def ordenar_tuplas(self):
        for cantidad_max_materias_por_cuatrimestre in self.datos:
            self.datos[cantidad_max_materias_por_cuatrimestre] = sorted(
                self.datos[cantidad_max_materias_por_cuatrimestre], key=lambda tupla: tupla[TUPLA_MAT_DISPONIBLES])


def cargar_datos(PLE, Greedy):
    with open('estadisticas_algoritmos.csv', 'r') as f:
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

def mostrar_grafico():
    plt.legend()
    plt.grid()
    plt.xlabel('Cantidad de Materias Disponibles')
    plt.ylabel('Tiempo [Segundos]')
    plt.show()

def graficar_mismo_algoritmo_con_cada_linea_cantidad_maxima_materias_diferente(algoritmo):
    plt.title('Tiempo algoritmo {} respecto de la máx. cant. de materias por cuatrimestre'.format(algoritmo.nombre))
    
    for cantidad_max_materias_por_cuatrimestre in algoritmo.datos:
        datos_x, datos_y = generar_datos_x_e_y_algoritmo(algoritmo.datos[cantidad_max_materias_por_cuatrimestre])
        label_linea = 'Max materias = {}'.format(cantidad_max_materias_por_cuatrimestre)
        plt.plot(datos_x, datos_y, label=label_linea)
    mostrar_grafico()

def generar_datos_x_e_y_algoritmo(datos_algoritmo):
    datos_x = []
    datos_y = []
    for tupla in datos_algoritmo:
        datos_x.append(tupla[TUPLA_MAT_DISPONIBLES])
        datos_y.append(tupla[TUPLA_SEGUNDOS])
    return datos_x, datos_y

def generar_grafico_algoritmos_combinados_para_cada_cantidad_maxima_de_materias_por_cuatrimestre(algoritmos):    
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

def generar_graficos_estadisticas():
    PLE = DatosAlgoritmo('PLE')
    Greedy = DatosAlgoritmo('Greedy')       
    cargar_datos(PLE, Greedy)

    PLE.ordenar_tuplas()
    Greedy.ordenar_tuplas()

    graficar_mismo_algoritmo_con_cada_linea_cantidad_maxima_materias_diferente(Greedy)
    graficar_mismo_algoritmo_con_cada_linea_cantidad_maxima_materias_diferente(PLE)

    generar_grafico_algoritmos_combinados_para_cada_cantidad_maxima_de_materias_por_cuatrimestre([PLE, Greedy])

generar_graficos_estadisticas()
