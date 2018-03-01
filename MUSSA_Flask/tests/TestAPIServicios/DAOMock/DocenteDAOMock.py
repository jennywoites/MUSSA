from app import db
from app.models.docentes_models import Docente, CursosDocente

##########################################################
##   Nombres de los parametros de los datos de prueba   ##
##########################################################

P_ID = "id"
P_APELLIDO = "apellido"
P_NOMBRE = "nombre"
P_NOMBRE_COMPLETO = "nombre_completo"
P_CURSOS_QUE_DICTA = "cursos_que_dicta"

##########################################################
##                    Datos de Prueba                   ##
##########################################################

DOCENTE_SIN_NOMBRE = {
    P_ID: -1,
    P_APELLIDO: "Apellido docente sin nombre",
    P_NOMBRE: "",
    P_NOMBRE_COMPLETO: "Apellido docente sin nombre",
    P_CURSOS_QUE_DICTA: []
}

DOCENTE_WOITES_JENNIFER = {
    P_ID: -1,
    P_APELLIDO: "Woites",
    P_NOMBRE: "Jennifer",
    P_NOMBRE_COMPLETO: "Woites, Jennifer",
    P_CURSOS_QUE_DICTA: []
}

class DocenteDAOMock:
    def crear_docente_sin_nombre(self):
        return self.crear_docente(DOCENTE_SIN_NOMBRE)

    def crear_docente_Woites_Jennifer(self):
        return self.crear_docente(DOCENTE_WOITES_JENNIFER)

    def crear_docente(self, datos):
        doc = Docente(
            apellido=datos[P_APELLIDO],
            nombre=datos[P_NOMBRE])
        db.session.add(doc)
        db.session.commit()
        return doc

    def agregar_curso_dictado(self, datos_docente, curso):
        db.session.add(CursosDocente(
            docente_id=datos_docente[P_ID],
            curso_id=curso.id
        ))
        db.session.commit()
        datos_docente[P_CURSOS_QUE_DICTA].append(curso.id)
