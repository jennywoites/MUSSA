from app import db
from app.models.carreras_models import Carrera, Creditos, Orientacion

LICENCIATURA_EN_SISTEMAS_1986 = {
    "codigo": "09",
    "nombre": "Licenciatura en Análisis de Sistemas",
    "plan": "1986",
    "duracion_estimada_en_cuatrimestres": 9,
    "requiere_prueba_suficiencia_de_idioma": False,
    "orientaciones": [],
    "creditos": {
        "creditos_obligatorias": 130,
        "creditos_electivas_general": 40,
        "creditos_orientacion": 0,
        "creditos_electivas_con_tp": 0,
        "creditos_electivas_con_tesis": 0,
        "creditos_tesis": 0,
        "creditos_tp_profesional": 0
    }
}

INGENIERIA_EN_INFORMATICA_1986 = {
    "codigo": "10",
    "nombre": "Ingeniería en Informática",
    "plan": "1986",
    "duracion_estimada_en_cuatrimestres": 12,
    "requiere_prueba_suficiencia_de_idioma": False,
    "orientaciones": [{
        "descripcion": 'Gestión Industrial de Sistemas',
        "clave_reducida": 'GESTION'
    }, {
        "descripcion": 'Sistemas Distribuidos',
        "clave_reducida": 'DISTRIBUIDOS'
    }, {
        "descripcion": 'Sistemas de Producción',
        "clave_reducida": 'PRODUCCION'
    }],
    "creditos": {
        "creditos_obligatorias": 156,
        "creditos_electivas_general": 0,
        "creditos_orientacion": 34,
        "creditos_electivas_con_tp": 46,
        "creditos_electivas_con_tesis": 34,
        "creditos_tesis": 24,
        "creditos_tp_profesional": 12
    }
}


class CarreraDAOMock:
    def crear_todas_las_carreras(self):
        self.crear_licenciatura_en_sistemas_1986()
        self.crear_ingenieria_informatica_1986()

    def crear_licenciatura_en_sistemas_1986(self):
        return self.crear_carrera(LICENCIATURA_EN_SISTEMAS_1986)

    def crear_ingenieria_informatica_1986(self):
        return self.crear_carrera(INGENIERIA_EN_INFORMATICA_1986)

    def crear_carrera(self, datos):
        carrera = self.agregar_carrera(datos)
        self.agregar_orientacion_a_carrera(carrera, datos["orientaciones"])
        self.agregar_creditos_carrera(carrera, datos["creditos"])
        return carrera

    def agregar_carrera(self, datos):
        carrera = Carrera(
            codigo=datos["codigo"],
            nombre=datos["nombre"],
            duracion_estimada_en_cuatrimestres=datos["duracion_estimada_en_cuatrimestres"],
            requiere_prueba_suficiencia_de_idioma=datos["requiere_prueba_suficiencia_de_idioma"],
        )
        db.session.add(carrera)
        db.session.commit()
        return carrera

    def agregar_orientacion_a_carrera(self, carrera, datos):
        for datos_orientacion in datos:
            db.session.add(Orientacion(
                descripcion=datos_orientacion["descripcion"],
                clave_reducida=datos_orientacion["clave_reducida"],
                carrera_id=carrera.id
            ))
            db.session.commit()

    def agregar_creditos_carrera(self, carrera, datos):
        creditos = Creditos(
            creditos_obligatorias=datos["creditos_obligatorias"],
            creditos_orientacion=datos["creditos_orientacion"],
            creditos_electivas_general=datos["creditos_electivas_general"],
            creditos_electivas_con_tp=datos["creditos_electivas_con_tp"],
            creditos_electivas_con_tesis=datos["creditos_electivas_con_tesis"],
            creditos_tesis=datos["creditos_tesis"],
            creditos_tp_profesional=datos["creditos_tp_profesional"]
        )
        db.session.add(creditos)
        db.session.commit()

        if not carrera.creditos:
            carrera.creditos = []

        carrera.creditos.append(creditos)
        db.session.commit()
