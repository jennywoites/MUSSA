from app.API_Rest.codes import *
from app.API_Rest.Services.BaseService import BaseService
from app.models.horarios_models import Curso
from app.models.carreras_models import Carrera
from app.models.generadorJSON.horarios_generadorJSON import generarJSON_curso_con_filtros
from app.models.generadorJSON.horarios_generadorJSON import obtener_carreras_response, obtener_docentes_response

class AllCursosService(BaseService):
    def getNombreClaseServicio(self):
        return "All Cursos Service"

    def get(self):
        self.logg_parametros_recibidos()

        nombre_curso = self.obtener_texto("nombre_curso")
        codigo_materia = self.obtener_parametro("codigo_materia")
        id_carrera = self.obtener_parametro("id_carrera")
        filtrar_cursos_dictados_en_algun_cuatrimestre = self.obtener_booleano("filtrar_cursos")

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            ("nombre_curso", {
                self.PARAMETRO: nombre_curso,
                self.ES_OBLIGATORIO: False,
                self.FUNCIONES_VALIDACION: [
                    (self.validar_contenido_y_longitud_texto, [1,15])
                ]}
             ),
            self.get_validaciones_codigo_materia("codigo_materia", codigo_materia, False),
            self.get_validaciones_entidad_basica("id_carrera", id_carrera, Carrera, False),
            ("filtrar_cursos_dictados_en_algun_cuatrimestre", {
                self.PARAMETRO: filtrar_cursos_dictados_en_algun_cuatrimestre,
                self.ES_OBLIGATORIO: False,
                self.FUNCIONES_VALIDACION: [
                    (self.booleano_es_valido, [])
                ]}
             )
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        query = Curso.query

        if nombre_curso: query = query.filter(Curso.codigo.like("%" + nombre_curso + "%"))
        if codigo_materia: query = query.filter(Curso.codigo_materia.like(codigo_materia + "%"))

        if filtrar_cursos_dictados_en_algun_cuatrimestre:
            query = query.filter((Curso.se_dicta_primer_cuatrimestre == True) | (Curso.se_dicta_segundo_cuatrimestre == True))

        cursos = query.all()

        cursos_result = []
        for curso in cursos:

            carreras_response = obtener_carreras_response(curso, id_carrera)

            if not carreras_response: #No es un curso valido para la query elegida
                continue

            docentes, docentes_response = obtener_docentes_response(curso)

            cursos_result.append(generarJSON_curso_con_filtros(
                curso,
                carreras_response,
                docentes,
                docentes_response
            ))

        cursos_result.sort(key=lambda curso : float(curso["puntaje"]), reverse=True)

        result = ({'cursos': cursos_result}, SUCCESS_OK)
        self.logg_resultado(result)

        return result


#########################################
CLASE = AllCursosService
URLS_SERVICIOS = (
    '/api/curso/all',
)
#########################################
