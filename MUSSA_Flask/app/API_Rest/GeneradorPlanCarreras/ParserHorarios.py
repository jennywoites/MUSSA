import PyPDF2

from app.API_Rest.GeneradorPlanCarreras.modelos.Curso import Curso
from app.API_Rest.GeneradorPlanCarreras.modelos.Horario import Horario

DIAS = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO", "DOMINGO"]

VOCALES = {
    'Á': 'A',
    'É': 'E',
    'Í': 'I',
    'Ó': 'O',
    'Ú': 'U'
}

CARRERAS = {
    'CIVIL': 1,
    'INDUSTRIAL': 2,
    'NAVAL': 3,
    'AGRIM': 4,
    'MECANICA': 5,
    'ELECTRICISTA': 6,
    'ELECTRONICA': 7,
    'QUIMICA': 8,
    'SISTEMAS': 9,
    'INFORMATICA': 10,
    'ALIMENTOS': 11,
    'ING. AGRIM': 12,
    'PETROLEO': 13
}


def parsear_carreras(linea):
    carreras = []
    linea = preparar_linea(linea)
    datos = linea.split(', ')
    for dato in datos:
        if dato == 'TODAS':
            return [x for x in range(1,len(CARRERAS)+1)]
        if dato in CARRERAS:
            carreras.append(CARRERAS[dato])
        else:
            print(dato)
            input("Error en la carrera!")

    return carreras


def preparar_linea(linea):
    linea = linea.upper()

    for vocal in VOCALES:
        while vocal in linea:
            linea = linea.replace(vocal, VOCALES[vocal])

    return linea


def get_posicion_horarios(linea):
    linea = preparar_linea(linea)

    min_pos = len(linea)
    for dia in DIAS:
        posicion = linea.find(dia)
        if posicion != -1 and posicion < min_pos:
            min_pos = posicion

    return min_pos if (min_pos != len(linea)) else -1


def obtener_todas_posiciones_de_dias(linea):
    posiciones = []
    linea_actual = preparar_linea(linea)
    for dia in DIAS:
        while dia in linea_actual:
            pos = linea_actual.find(dia)
            if pos == -1: continue
            posiciones.append(pos)
            linea_actual = linea_actual[:pos] + ("X" * len(dia)) + linea_actual[pos+len(dia):]
    return posiciones


def procesar_horarios(linea):
    horarios = []
    for datos in linea:
        datos = preparar_linea(datos)
        d_horarios = ""
        d_dia = ""

        for dia in DIAS:
            if dia in datos:
                d_horarios = datos[len(dia):]
                d_dia = dia
                break

        len_horario = 5  #ej 19:00
        hora_desde = procesar_hora(d_horarios[:len_horario])
        d_horarios = d_horarios[len_horario + 1:]
        hora_hasta = procesar_hora(d_horarios[:len_horario])

        horario = (d_dia, hora_desde, hora_hasta)
        horarios.append(horario)

    return horarios


def procesar_hora(hora_string):
    """Recibe una hora como un string con el siguiente formato:
    19:00. Si la hora no es en punto, se agrega 0,5 como valor
    a la cantidad de horas"""
    horas, minutos = hora_string.split(":")
    return int(horas) + (0.5 if int(minutos) > 0 else 0) 


def parsear_horarios(linea):
    horarios = []
    posicion_dias = obtener_todas_posiciones_de_dias(linea)
    posicion_dias.sort()
    posicion_dias.pop(0) #Descarto la posicion 0 que es siempre la primera

    offset = 0
    for pos in posicion_dias:
        horario = linea[:pos-offset]

        horarios.append(horario)
        linea = linea[pos-offset:]
        offset += len(horario)

    horarios.append(linea)

    return procesar_horarios(horarios)


def parsear_materia(materia):
    codigo = ""
    for c in materia:
        if c == " ":
            break
        codigo += c
    return codigo, materia[len(codigo)+1:]


def parsear_horarios_de_materias(texto):
    horarios_materias = []
    datos = texto.split("Materia: ")

    for dato in datos:
        try:
            materia, mas_datos = dato.split("Vacantes: ")
            codigo, nombre_materia = parsear_materia(materia)
            vacantes, mas_datos = mas_datos.split("Docente: ")
            docentes, mas_datos = mas_datos.split("Carreras: ")
            carreras, mas_datos = mas_datos.split("Curso: ")
            carreras = parsear_carreras(carreras)

            pos_horarios = get_posicion_horarios(mas_datos)

            if pos_horarios == -1:
                raise Exception("No hay horarios")

            curso = mas_datos[:pos_horarios]
            horarios = parsear_horarios(mas_datos[pos_horarios:])

            horario_materia = {
                'Codigo': codigo,
                'Materia': nombre_materia,
                'Vacantes': vacantes,
                'Docentes': docentes,
                'Carreras': carreras,
                'Curso': curso,
                'Horarios': horarios
            }

            horarios_materias.append(horario_materia)

        except ValueError as error:
            print(error)

    return horarios_materias


def parsear_pdf(ruta):
    pdfFileObj = open(ruta,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    texto = ""
    for i in range(0, pdfReader.numPages):
        pageObj = pdfReader.getPage(i)
        texto += pageObj.extractText()

    return parsear_horarios_de_materias(texto)