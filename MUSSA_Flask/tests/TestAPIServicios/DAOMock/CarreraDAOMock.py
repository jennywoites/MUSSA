from app import db
from app.models.carreras_models import Carrera, Creditos, Orientacion

##########################################################
##   Nombres de los parametros de los datos de prueba   ##
##########################################################

P_ID = "id"
P_CODIGO = "codigo"
P_NOMBRE = "nombre"
P_PLAN = "plan"
P_DURACION_EN_CUATRIMESTRES = "duracion_estimada_en_cuatrimestres"
P_REQUIERE_PRUEBA_SUF_IDIOMA = "requiere_prueba_suficiencia_de_idioma"
P_ORIENTACIONES = "orientaciones"
P_DESCRIPCION = "descripcion"
P_CLAVE_REDUCIDA = "clave_reducida"
P_CREDITOS = "creditos"
P_CREDITOS_OBLIGATORIAS = "creditos_obligatorias"
P_CREDITOS_ELECTIVAS_GRAL = "creditos_electivas_general"
P_CREDITOS_ORIENTACION = "creditos_orientacion"
P_CREDITOS_ELECTIVAS_CON_TP = "creditos_electivas_con_tp"
P_CREDITOS_ELECTIVAS_CON_TESIS = "creditos_electivas_con_tesis"
P_CREDITOS_TESIS = "creditos_tesis"
P_CREDITOS_TP_PROFESIONAL = "creditos_tp_profesional"

##########################################################
##                    Datos de Prueba                   ##
##########################################################

LICENCIATURA_EN_SISTEMAS_1986 = {
    P_ID: -1,
    P_CODIGO: "09",
    P_NOMBRE: "Licenciatura en Análisis de Sistemas",
    P_PLAN: "1986",
    P_DURACION_EN_CUATRIMESTRES: 9,
    P_REQUIERE_PRUEBA_SUF_IDIOMA: False,
    P_ORIENTACIONES: [],
    P_CREDITOS: {
        P_CREDITOS_OBLIGATORIAS: 130,
        P_CREDITOS_ELECTIVAS_GRAL: 40,
        P_CREDITOS_ORIENTACION: 0,
        P_CREDITOS_ELECTIVAS_CON_TP: 0,
        P_CREDITOS_ELECTIVAS_CON_TESIS: 0,
        P_CREDITOS_TESIS: 0,
        P_CREDITOS_TP_PROFESIONAL: 0
    }
}

INGENIERIA_EN_INFORMATICA_1986 = {
    P_ID: -1,
    P_CODIGO: "10",
    P_NOMBRE: "Ingeniería en Informática",
    P_PLAN: "1986",
    P_DURACION_EN_CUATRIMESTRES: 12,
    P_REQUIERE_PRUEBA_SUF_IDIOMA: False,
    P_ORIENTACIONES: [
        {
            P_DESCRIPCION: 'Gestión Industrial de Sistemas',
            P_CLAVE_REDUCIDA: 'GESTION'
        }, {
            P_DESCRIPCION: 'Sistemas Distribuidos',
            P_CLAVE_REDUCIDA: 'DISTRIBUIDOS'
        }, {
            P_DESCRIPCION: 'Sistemas de Producción',
            P_CLAVE_REDUCIDA: 'PRODUCCION'
        }
    ],
    P_CREDITOS: {
        P_CREDITOS_OBLIGATORIAS: 156,
        P_CREDITOS_ELECTIVAS_GRAL: 0,
        P_CREDITOS_ORIENTACION: 34,
        P_CREDITOS_ELECTIVAS_CON_TP: 46,
        P_CREDITOS_ELECTIVAS_CON_TESIS: 34,
        P_CREDITOS_TESIS: 24,
        P_CREDITOS_TP_PROFESIONAL: 12
    }
}

CARRERA_FICTICIA_1 = {
    P_ID: -1,
    P_CODIGO: "88",
    P_NOMBRE: "Carrera Ficticia 1",
    P_PLAN: "2018",
    P_DURACION_EN_CUATRIMESTRES: 9,
    P_REQUIERE_PRUEBA_SUF_IDIOMA: False,
    P_ORIENTACIONES: [],
    P_CREDITOS: {
        P_CREDITOS_OBLIGATORIAS: 130,
        P_CREDITOS_ELECTIVAS_GRAL: 40,
        P_CREDITOS_ORIENTACION: 0,
        P_CREDITOS_ELECTIVAS_CON_TP: 0,
        P_CREDITOS_ELECTIVAS_CON_TESIS: 0,
        P_CREDITOS_TESIS: 0,
        P_CREDITOS_TP_PROFESIONAL: 0
    }
}

class CarreraDAOMock:
    def crear_licenciatura_en_sistemas_1986(self):
        return self.crear_carrera(LICENCIATURA_EN_SISTEMAS_1986)

    def crear_ingenieria_informatica_1986(self):
        return self.crear_carrera(INGENIERIA_EN_INFORMATICA_1986)

    def crear_carrera_ficticia_1(self):
        return self.crear_carrera(CARRERA_FICTICIA_1)

    def crear_carrera(self, datos):
        carrera = self.agregar_carrera(datos)
        datos[P_ID] = carrera.id

        self.agregar_orientacion_a_carrera(carrera, datos[P_ORIENTACIONES])
        self.agregar_creditos_carrera(carrera, datos[P_CREDITOS])
        return carrera

    def agregar_carrera(self, datos):
        carrera = Carrera(
            codigo=datos[P_CODIGO],
            nombre=datos[P_NOMBRE],
            duracion_estimada_en_cuatrimestres=datos[P_DURACION_EN_CUATRIMESTRES],
            requiere_prueba_suficiencia_de_idioma=datos[P_REQUIERE_PRUEBA_SUF_IDIOMA],
        )
        db.session.add(carrera)
        db.session.commit()
        return carrera

    def agregar_orientacion_a_carrera(self, carrera, datos):
        for datos_orientacion in datos:
            db.session.add(Orientacion(
                descripcion=datos_orientacion[P_DESCRIPCION],
                clave_reducida=datos_orientacion[P_CLAVE_REDUCIDA],
                carrera_id=carrera.id
            ))
            db.session.commit()

    def agregar_creditos_carrera(self, carrera, datos):
        creditos = Creditos(
            creditos_obligatorias=datos[P_CREDITOS_OBLIGATORIAS],
            creditos_orientacion=datos[P_CREDITOS_ORIENTACION],
            creditos_electivas_general=datos[P_CREDITOS_ELECTIVAS_GRAL],
            creditos_electivas_con_tp=datos[P_CREDITOS_ELECTIVAS_CON_TP],
            creditos_electivas_con_tesis=datos[P_CREDITOS_ELECTIVAS_CON_TESIS],
            creditos_tesis=datos[P_CREDITOS_TESIS],
            creditos_tp_profesional=datos[P_CREDITOS_TP_PROFESIONAL]
        )
        db.session.add(creditos)
        db.session.commit()

        if not carrera.creditos:
            carrera.creditos = []

        carrera.creditos.append(creditos)
        db.session.commit()
