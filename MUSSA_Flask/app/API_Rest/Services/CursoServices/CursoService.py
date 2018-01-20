from flask_user import roles_accepted
from app.API_Rest.Services.BaseService import BaseService
from app.models.generadorJSON.horarios_generadorJSON import generarJSON_curso
from app.models.horarios_models import Curso, HorarioPorCurso, CarreraPorCurso, Horario
from app.API_Rest.codes import *
from app.models.carreras_models import Carrera
from app.models.docentes_models import Docente, CursosDocente
from app import db


class CursoService(BaseService):
    def getNombreClaseServicio(self):
        return "Curso Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    def get(self, idCurso):
        return self.servicio_get_base(idCurso, "idCurso", Curso, generarJSON_curso)

    @roles_accepted('admin')
    def delete(self, idCurso):
        self.servicio_delete_base(idCurso, "idCurso", Curso)

    @roles_accepted('admin')
    def post(self, idCurso):
        self.logg_parametros_recibidos()

        ids_carreras = self.obtener_lista("ids_carreras")
        se_dicta_primer_cuatrimestre = self.obtener_booleano("primer_cuatrimestre")
        se_dicta_segundo_cuatrimestre = self.obtener_booleano("segundo_cuatrimestre")
        ids_docentes = self.obtener_lista("ids_docentes")
        horarios = self.obtener_lista_de_horarios("horarios")

        if not ids_carreras or not ids_docentes or not horarios:
            msj = 'El curso debe tener carreras, docentes y horarios válidos'
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_BAD_REQUEST

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            self.get_validaciones_entidad_basica("idCurso", idCurso, Curso),
            self.get_validaciones_entidad_basica("ids_carreras", ids_carreras, Carrera),
            ("se_dicta_primer_cuatrimestre", {
                self.PARAMETRO: se_dicta_primer_cuatrimestre,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.booleano_es_valido, [])
                ]
            }),
            ("se_dicta_segundo_cuatrimestre", {
                self.PARAMETRO: se_dicta_segundo_cuatrimestre,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.booleano_es_valido, [])
                ]
            }),
            self.get_validaciones_entidad_basica("ids_docentes", ids_docentes, Docente),
            ("horarios", {
                self.PARAMETRO: horarios,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.horario_es_valido, [])
                ]
            })
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        curso = Curso.query.get(idCurso)

        self.eliminar_horarios_viejos(idCurso)
        self.eliminar_carreras_asociadas_viejas(idCurso)
        self.eliminar_docentes_actuales(idCurso)

        curso.se_dicta_primer_cuatrimestre = se_dicta_primer_cuatrimestre
        curso.se_dicta_segundo_cuatrimestre = se_dicta_segundo_cuatrimestre

        db.session.commit()

        self.agregar_horarios(idCurso, horarios)
        self.agregar_carreras(idCurso, ids_carreras)
        self.agregar_docentes(idCurso, ids_docentes)

        result = SUCCESS_OK
        self.logg_resultado(result)

        return result

    def eliminar_horarios_viejos(self, id_curso):
        horarios_por_curso = HorarioPorCurso.query.filter_by(curso_id=id_curso).all()

        ids_horarios = []
        for h in horarios_por_curso:
            ids_horarios.append(h.horario_id)

        HorarioPorCurso.query.filter_by(curso_id=id_curso).delete()
        db.session.commit()

        for id_horario in ids_horarios:
            Horario.query.filter_by(id=id_horario).delete()

        db.session.commit()

    def eliminar_carreras_asociadas_viejas(self, id_curso):
        CarreraPorCurso.query.filter_by(curso_id=id_curso).delete()
        db.session.commit()

    def eliminar_docentes_actuales(self, id_curso):
        CursosDocente.query.filter_by(curso_id=id_curso).delete()
        db.session.commit()

    def agregar_horarios(self, id_curso, horarios):
        for horario_a_agregar in horarios:
            horario = Horario(
                dia=horario_a_agregar["dia"],
                hora_desde=horario_a_agregar["hora_desde"],
                hora_hasta=horario_a_agregar["hora_hasta"],
            )
            db.session.add(horario)
            db.session.commit()

            db.session.add(HorarioPorCurso(curso_id=id_curso, horario_id=horario.id))

        db.session.commit()

    def agregar_docentes(self, id_curso, ids_docentes):
        for id_docente in ids_docentes:
            db.session.add(CursosDocente(
                curso_id=id_curso,
                docente_id=id_docente
            ))
        db.session.commit()

    def agregar_carreras(self, id_curso, carreras):
        for id_carrera in carreras:
            db.session.add(CarreraPorCurso(curso_id=id_curso, carrera_id=int(id_carrera)))
            db.session.commit()


#########################################
CLASE = CursoService
URLS_SERVICIOS = (
    '/api/curso/<int:idCurso>',
)
#########################################
