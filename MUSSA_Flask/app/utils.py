from datetime import datetime

LUNES = "LUNES"
MARTES = "MARTES"
MIERCOLES = "MIERCOLES"
JUEVES = "JUEVES"
VIERNES = "VIERNES"
SABADO = "SABADO"

DIAS = [LUNES, MARTES, MIERCOLES, JUEVES, VIERNES, SABADO]


#####################################################################

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'

    class K:
        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

    return K


#####################################################################
def sustituir_todos_los_acentos(linea):
    ACENTOS = {
        'Á': 'A',
        'É': 'E',
        'Í': 'I',
        'Ó': 'O',
        'Ú': 'U',
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u'
    }
    nueva_linea = linea
    for vocal in ACENTOS:
        while(vocal in nueva_linea):
            nueva_linea = nueva_linea.replace(vocal, ACENTOS[vocal])
    return nueva_linea

def generar_lista_anios():
    MAX_TIEMPO = 5
    hoy = datetime.now().year
    return [x for x in range(hoy, hoy - MAX_TIEMPO, -1)]


def generar_lista_horarios():
    HORA_MIN = 7
    HORA_MAX = 23
    horarios = []
    for i in frange(HORA_MIN, HORA_MAX + 0.5, 0.5):
        hora = int(i)
        minutos = "00" if hora == i else "30"
        horarios.append("{}:{}".format(get_numero_dos_digitos(hora), minutos))
    return horarios


def convertir_horario(horas, minutos):
    c_hora = int(horas)
    c_hora += 0.5 if int(minutos) == 30 else 0
    return c_hora


def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step


def get_numero_dos_digitos(num):
    num = str(num)
    if len(num) < 2:
        return "0{}".format(num)
    return num
