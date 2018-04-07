from app.API_Rest.codes import *
from app.models.docentes_models import Docente, CursosDocente
from app.API_Rest.Services.BaseService import BaseService
from flask_user import roles_accepted
from app import db
from app.models.respuestas_encuesta_models import RespuestaEncuestaDocente


class AgruparDocentesService(BaseService):
    def getNombreClaseServicio(self):
        return "Agrupar Docentes Service"

    @roles_accepted('admin')
    def post(self):
        """
        Agrupa los docentes de los ids seleccionados tomando el
        apellido del primero  el primer nombre no nulo (si ninguno
        posee nombre queda vacío). Agrega como cursos (sin repetir)
        la unión de los cursos de todos ellos.
        """
        self.logg_parametros_recibidos()

        ids_docentes = self.obtener_lista("ids_docentes")

        if len(ids_docentes) < 2:
            msj = "Se requieren al menos dos docentes a agrupar"
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_BAD_REQUEST

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            ("ids_docentes", {
                self.PARAMETRO: ids_docentes,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.id_es_valido, []),
                    (self.existe_id, [Docente])
                ]
            })
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        datos = {
            "apellido": '',
            "nombre": '',
            "ids_cursos": {}
        }

        for id_docente in ids_docentes:
            docente = Docente.query.get(id_docente)

            if not datos["apellido"]:
                datos["apellido"] = docente.apellido

            if not datos["nombre"] and docente.nombre:
                datos["nombre"] = docente.nombre

            cursos = CursosDocente.query.filter_by(docente_id=id_docente).all()
            for curso in cursos:
                if curso.curso_id not in datos["ids_cursos"]:
                    datos["ids_cursos"][curso.curso_id] = ''
            CursosDocente.query.filter_by(docente_id=id_docente).delete()
            db.session.commit()

        id_docente_agrupado = ids_docentes[0]

        self.actualizar_encuestas_para_que_referencien_al_docente_agrupado(ids_docentes, id_docente_agrupado)
        self.eliminar_los_otros_docentes(ids_docentes)
        self.actualizar_datos_unico_docente_agrupado(id_docente_agrupado, datos)

        result = SUCCESS_NO_CONTENT
        self.logg_resultado(result)
        return result

    def actualizar_encuestas_para_que_referencien_al_docente_agrupado(self, ids_docentes, id_docente_agrupado):
        encuestas_a_actualizar = RespuestaEncuestaDocente.query \
            .filter(RespuestaEncuestaDocente.docente_id.in_(ids_docentes)).all()
        for encuesta in encuestas_a_actualizar:
            encuesta.docente_id = id_docente_agrupado
            db.session.commit()

    def eliminar_los_otros_docentes(self, ids_docentes):
        # No es borrado logico sino que se los quita de la bdd porque pasan a ser uno solo
        for i in range(1, len(ids_docentes)):
            Docente.query.filter_by(id=ids_docentes[i]).delete()
            db.session.commit()

    def actualizar_datos_unico_docente_agrupado(self, id_docente, datos):
        docente = Docente.query.get(id_docente)
        docente.apellido = datos["apellido"]
        docente.nombre = datos["nombre"]
        db.session.commit()

        for id_curso in datos["ids_cursos"]:
            db.session.add(CursosDocente(
                docente_id=id_docente,
                curso_id=id_curso
            ))
            db.session.commit()


#########################################
CLASE = AgruparDocentesService
URLS_SERVICIOS = (
    '/api/docente/agrupar',
)
#########################################
