if __name__ == '__main__':
    import sys

    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase
from app.models.carreras_models import Carrera, Materia, TipoMateria
from app.models.alumno_models import Alumno, EstadoMateria, MateriasAlumno
from app.DAO.MateriasDAO import *
from app.API_Rest.services import *
from app.API_Rest.codes import *


class TestAgregarMateriaAlumno(TestBase):
    ##########################################################
    ##                   Configuracion                      ##
    ##########################################################

    def get_test_name(self):
        return "test_agregar_materia_alumno"

    def crear_datos_bd(self):
        carrera = Carrera(
            codigo='9',
            nombre='Licenciatura en Análisis de Sistemas',
            duracion_estimada_en_cuatrimestres=9,
            requiere_prueba_suficiencia_de_idioma=False
        )
        db.session.add(carrera)

        tipo_materia = TipoMateria(descripcion="Tipo Materia Test")
        db.session.add(tipo_materia)
        db.session.commit()

        materia = Materia(
            codigo="7514",
            nombre="Materia Test",
            creditos_minimos_para_cursarla=0,
            creditos=0,
            tipo_materia_id=tipo_materia.id,
            carrera_id=carrera.id
        )
        db.session.add(materia)

        alumno = Alumno(user_id=self.get_usuario().id)
        db.session.add(alumno)
        db.session.commit()

        admin_alumno = Alumno(user_id=self.get_administrador().id)
        db.session.add(admin_alumno)
        db.session.commit()

        estado = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[PENDIENTE]).first()

        db.session.add(MateriasAlumno(
            alumno_id=alumno.id,
            materia_id=materia.id,
            carrera_id=carrera.id,
            estado_id=estado.id,
        ))

        db.session.add(MateriasAlumno(
            alumno_id=admin_alumno.id,
            materia_id=materia.id,
            carrera_id=carrera.id,
            estado_id=estado.id,
        ))

    ##########################################################
    ##                      Tests                           ##
    ##########################################################

    def test_agregar_materia_sin_estar_logueado_da_error(self):
        client = self.app.test_client()
        response = client.post(AGREGAR_MATERIA_ALUMNO_SERVICE)
        assert (response.status_code == REDIRECTION_FOUND)

    def test_agregar_materia_logueado_con_administrador_es_exitosa(self):
        client = self.loguear_administrador()

        estado = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[EN_CURSO]).first()
        parametros = {}
        parametros["id_carrera"] = Carrera.query.first().id
        parametros["id_materia"] = Materia.query.first().id
        parametros["estado"] = estado.estado

        response = client.post(AGREGAR_MATERIA_ALUMNO_SERVICE, data=parametros)

        assert (response.status_code == SUCCESS_OK)

    def test_agregar_materia_en_curso_con_parametros_correctos(self):
        client = self.loguear_usuario()

        materia_alumno_original = MateriasAlumno.query.first()
        id_original = materia_alumno_original.id
        alumno_id_original = materia_alumno_original.alumno_id
        materia_id_original = materia_alumno_original.materia_id
        carrera_id_original = materia_alumno_original.carrera_id

        estado = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[EN_CURSO]).first()

        parametros = {}
        parametros["id_carrera"] = Carrera.query.first().id
        parametros["id_materia"] = Materia.query.first().id
        parametros["estado"] = estado.estado

        response = client.post(AGREGAR_MATERIA_ALUMNO_SERVICE, data=parametros)

        assert (response.status_code == SUCCESS_OK)

        materia_alumno = MateriasAlumno.query.first()

        assert (materia_alumno.id == id_original)
        assert (materia_alumno.alumno_id == alumno_id_original)
        assert (materia_alumno.materia_id == materia_id_original)
        assert (materia_alumno.carrera_id == carrera_id_original)

        assert (materia_alumno.estado_id == estado.id)

        assert (materia_alumno.calificacion is None)
        assert (materia_alumno.fecha_aprobacion is None)
        assert (materia_alumno.cuatrimestre_aprobacion_cursada is None)
        assert (materia_alumno.anio_aprobacion_cursada is None)
        assert (materia_alumno.acta_o_resolucion == "")
        assert (materia_alumno.forma_aprobacion_id is None)


if __name__ == '__main__':
    import unittest

    unittest.main()
