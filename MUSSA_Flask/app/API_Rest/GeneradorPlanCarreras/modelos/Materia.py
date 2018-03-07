from app.API_Rest.GeneradorPlanCarreras.Constantes import *


class Materia:
    def __init__(self, id_materia, codigo, nombre, creditos, tipo, cred_min=0, correlativas=[],
                 tematicas_principales=[], medias_horas_extras_cursada=0):
        self.id_materia = id_materia
        self.codigo = codigo
        self.nombre = nombre
        self.creditos = creditos
        self.tipo = tipo
        self.creditos_minimos_aprobados = cred_min
        self.correlativas = correlativas
        self.tematicas_principales = tematicas_principales
        self.medias_horas_extras_cursada = medias_horas_extras_cursada

    def generar_JSON(self):
        return {
            "id_materia": self.id_materia,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "creditos": self.creditos,
            "tipo": self.tipo,
            "creditos_minimos_aprobados": self.creditos_minimos_aprobados,
            "correlativas": self.correlativas[:],
            "tematicas_principales": self.tematicas_principales[:],
            "medias_horas_extras_cursada": self.medias_horas_extras_cursada,
        }

    def actualizar_datos_desde_JSON(self, datos_json):
        self.id_materia = datos_json["id_materia"]
        self.codigo = datos_json["codigo"]
        self.nombre = datos_json["nombre"]
        self.creditos = datos_json["creditos"]
        self.tipo = datos_json["tipo"]
        self.creditos_minimos_aprobados = datos_json["creditos_minimos_aprobados"]
        self.correlativas = datos_json["correlativas"]
        self.tematicas_principales = datos_json["tematicas_principales"]
        self.medias_horas_extras_cursada = datos_json["medias_horas_extras_cursada"]

    def copia_profunda(self):
        return Materia(
            id_materia=self.id_materia,
            codigo=self.codigo,
            nombre=self.nombre,
            creditos=self.creditos,
            tipo=self.tipo,
            cred_min=self.creditos_minimos_aprobados,
            correlativas=self.correlativas[:],
            tematicas_principales=self.tematicas_principales[:],
            medias_horas_extras_cursada=self.medias_horas_extras_cursada
        )

    def get_str_tipo(self):
        return TIPOS_MATERIAS[self.tipo]

    def __str__(self):
        return "{} - {} - {} - {} min aprobados - {}".format(self.codigo, self.nombre, self.creditos,
                                                             self.creditos_minimos_aprobados, self.correlativas)
