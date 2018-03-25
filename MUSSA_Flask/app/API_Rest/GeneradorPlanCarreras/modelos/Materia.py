from app.API_Rest.GeneradorPlanCarreras.Constantes import *
import hashlib


class Materia:
    def inicializar_con_JSON(self, datos_json):
        self.id_materia = int(datos_json["id_materia"])
        self.codigo = datos_json["codigo"]
        self.nombre = datos_json["nombre"]
        self.creditos = int(datos_json["creditos"])
        self.tipo = datos_json["tipo"]
        self.creditos_minimos_aprobados = int(datos_json["creditos_minimos_aprobados"])

        self.correlativas = []
        for id_correlativa in datos_json["correlativas"]:
            self.correlativas.append(int(id_correlativa))

        self.tematicas_principales = []
        for id_tematica in datos_json["tematicas_principales"]:
            self.tematicas_principales.append(int(id_tematica))

        self.medias_horas_extras_cursada = int(datos_json["medias_horas_extras_cursada"])

    def __init__(self, id_materia='', codigo='', nombre='', creditos=0, tipo='', cred_min=0, correlativas=[],
                 tematicas_principales=[], medias_horas_extras_cursada=0, datos_JSON=''):
        if datos_JSON:
            return self.inicializar_con_JSON(datos_JSON)

        self.id_materia = id_materia
        self.codigo = codigo
        self.nombre = nombre
        self.creditos = creditos
        self.tipo = tipo
        self.creditos_minimos_aprobados = cred_min
        self.correlativas = correlativas
        self.tematicas_principales = tematicas_principales
        self.medias_horas_extras_cursada = medias_horas_extras_cursada

    def __str__(self):
        SALTO = "\n"
        materia = "{" + SALTO
        materia += "id_materia:" + str(self.id_materia) + SALTO
        materia += "codigo:" + str(self.codigo) + SALTO
        materia += "nombre:" + str(self.nombre) + SALTO
        materia += "creditos:" + str(self.creditos) + SALTO
        materia += "tipo:" + str(self.tipo) + SALTO
        materia += "creditos_minimos_aprobados:" + str(self.creditos_minimos_aprobados) + SALTO
        materia += "correlativas:" + str(self.correlativas) + SALTO
        materia += "tematicas_principales:" + str(self.tematicas_principales) + SALTO
        materia += "medias_horas_extras_cursada:" + str(self.medias_horas_extras_cursada) + SALTO
        materia += "}" + SALTO
        return materia

    def obtener_hash_materia(self):
        SEPARADOR = "||"
        materia = "Materia : {"
        materia += "id_materia: {}".format(self.id_materia) + SEPARADOR
        materia += "codigo: {}".format(self.codigo) + SEPARADOR
        materia += "nombre: {}".format(self.nombre) + SEPARADOR
        materia += "creditos: {}".format(self.creditos) + SEPARADOR
        materia += "tipo: {}".format(self.tipo) + SEPARADOR
        materia += "creditos_minimos_aprobados: {}".format(self.creditos_minimos_aprobados) + SEPARADOR
        materia += "correlativas: {}".format(sorted(self.correlativas)) + SEPARADOR
        materia += "tematicas_principales: {}".format(self.tematicas_principales) + SEPARADOR
        materia += "medias_horas_extras_cursada: {}".format(self.medias_horas_extras_cursada) + SEPARADOR
        materia += "}"
        return hashlib.sha1(materia.encode('utf-8'))

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
