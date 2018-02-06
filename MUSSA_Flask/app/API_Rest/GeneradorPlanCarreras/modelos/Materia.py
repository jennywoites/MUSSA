from app.API_Rest.GeneradorPlanCarreras.Constantes import *

class Materia:

    def __init__(self, codigo, nombre, creditos, tipo, cred_min=0, correlativas=[]):
        self.codigo = codigo
        self.nombre = nombre
        self.creditos = creditos
        self.tipo = tipo
        self.creditos_minimos_aprobados = cred_min
        self.correlativas = correlativas

    def get_str_tipo(self):
    	return TIPOS_MATERIAS[self.tipo]

    def __str__(self):
        return "{} - {} - {} - {} min aprobados - {}".format(self.codigo, self.nombre, self.creditos, self.creditos_minimos_aprobados, self.correlativas)
