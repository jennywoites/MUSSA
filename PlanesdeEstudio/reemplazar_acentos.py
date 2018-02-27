VOCALES = {
    'Á': 'A',
    'É': 'E',
    'Í': 'I',
    'Ó': 'O',
    'Ú': 'U'
}

def reemplazar_acentos_linea(linea):
    nueva_linea = linea
    for vocal in VOCALES:
        while(vocal in nueva_linea):
            nueva_linea = nueva_linea.replace(vocal, VOCALES[vocal])
    return nueva_linea

def actualizar_archivo(ruta):
    lineas_nuevas = []
    with open(ruta, 'r') as archivo:
        for linea in archivo:
            lineas_nuevas.append(reemplazar_acentos_linea(linea))

    with open(ruta, 'w') as archivo:
        archivo.writelines(lineas_nuevas)

    
actualizar_archivo('ingenieria_en_informatica_1986.csv')
actualizar_archivo('licenciatura_en_analisis_de_sistemas_1986.csv')
