if __name__ == '__main__':
    import sys

    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase

from app import db
from app.models.horarios_models import Curso, Horario, HorarioPorCurso, CarreraPorCurso
from app.models.carreras_models import Carrera

import datetime

from app.API_Rest.services import *
from app.API_Rest.codes import *


class TestModificarCurso(TestBase):
    ##########################################################
    ##                   Configuracion                      ##
    ##########################################################

    FECHA = datetime.datetime.now()

    CARRERA_1 = {
        "id": 1,
        "codigo": "10",
        "nombre": 'Ingeniería en Informática',
        "duracion_estimada_en_cuatrimestres": 12,
        "requiere_prueba_suficiencia_de_idioma": False
    }

    CARRERA_2 = {
        "id": 2,
        "codigo": "9",
        "nombre": 'Otra carrera test',
        "duracion_estimada_en_cuatrimestres": 8,
        "requiere_prueba_suficiencia_de_idioma": True
    }

    CARRERA_3 = {
        "id": 3,
        "codigo": "25",
        "nombre": 'Nueva carrera test',
        "duracion_estimada_en_cuatrimestres": 10,
        "requiere_prueba_suficiencia_de_idioma": False
    }

    def get_carreras_bd(self):
        return [self.CARRERA_1, self.CARRERA_2, self.CARRERA_3]

    HORARIO_1 = {
        "id": 1,
        "dia": "Lunes",
        "hora_desde": "7.5",
        "hora_hasta": "11",
        "hora_desde_reloj": "07:30",
        "hora_hasta_reloj": "11:00"
    }

    HORARIO_2 = {
        "id": 2,
        "dia": "Jueves",
        "hora_desde": "16",
        "hora_hasta": "21",
        "hora_desde_reloj": "16:00",
        "hora_hasta_reloj": "21:00"
    }

    HORARIO_3 = {
        "id": 3,
        "dia": "Viernes",
        "hora_desde": "7.5",
        "hora_hasta": "13",
        "hora_desde_reloj": "07:30",
        "hora_hasta_reloj": "13:00"
    }

    HORARIO_4 = {
        "id": 4,
        "dia": "Viernes",
        "hora_desde": "7.5",
        "hora_hasta": "13",
        "hora_desde_reloj": "07:30",
        "hora_hasta_reloj": "13:00"
    }

    def get_horarios_bd(self):
        return [self.HORARIO_1, self.HORARIO_2]

    CURSO = {
        "id": 1,
        "codigo_materia": "7540",
        "codigo": "7540-CursoA",
        "docentes": "Doc1",
        "se_dicta_primer_cuatrimestre": True,
        "se_dicta_segundo_cuatrimestre": True,
        "cuatrimestre": "Ambos cuatrimestres",
        "cantidad_encuestas_completas": 20,
        "puntaje_total_encuestas": 105,
        "fecha_actualizacion": FECHA,
        "horarios": [HORARIO_1, HORARIO_2],
        "carreras": [CARRERA_1, CARRERA_2]
    }

    def get_test_name(self):
        return "test_buscar_cursos"

    def crear_datos_bd(self):
        for carrera in self.get_carreras_bd():
            self.agregar_carrera(carrera)

        for horario in self.get_horarios_bd():
            self.agregar_horario(horario)

        self.agregar_curso(self.CURSO)

        for c_horario in self.CURSO["horarios"]:
            self.agregar_horario_por_curso(self.CURSO, c_horario)

        for c_carrera in self.CURSO["carreras"]:
            self.agregar_carrera_por_curso(self.CURSO, c_carrera)

    def agregar_carrera(self, datos):
        db.session.add(Carrera(
            codigo=datos["codigo"],
            nombre=datos["nombre"],
            duracion_estimada_en_cuatrimestres=datos["duracion_estimada_en_cuatrimestres"],
            requiere_prueba_suficiencia_de_idioma=datos["requiere_prueba_suficiencia_de_idioma"]
        ))
        db.session.commit()

    def agregar_curso(self, datos):
        db.session.add(Curso(
            codigo_materia=datos["codigo_materia"],
            codigo=datos["codigo"],
            docentes=datos["docentes"],
            se_dicta_primer_cuatrimestre=datos["se_dicta_primer_cuatrimestre"],
            se_dicta_segundo_cuatrimestre=datos["se_dicta_segundo_cuatrimestre"],
            cantidad_encuestas_completas=datos["cantidad_encuestas_completas"],
            puntaje_total_encuestas=datos["puntaje_total_encuestas"],
            fecha_actualizacion=datos["fecha_actualizacion"],
        ))
        db.session.commit()

    def agregar_horario(self, datos):
        db.session.add(Horario(
            dia=datos["dia"],
            hora_desde=datos["hora_desde"],
            hora_hasta=datos["hora_hasta"]
        ))
        db.session.commit()

    def agregar_horario_por_curso(self, curso, horario):
        db.session.add(HorarioPorCurso(
            curso_id=curso["id"],
            horario_id=horario["id"]
        ))
        db.session.commit()

    def agregar_carrera_por_curso(self, curso, carrera):
        db.session.add(CarreraPorCurso(
            curso_id=curso["id"],
            carrera_id=carrera["id"]
        ))
        db.session.commit()

    def obtener_carreras_formateadas(self, l_carreras):
        carreras = ""
        for c in l_carreras:
            carreras += str(c["id"]) + ";"
        return carreras[:-1]

    def obtener_docentes_formateados(self, curso):
        return curso["docentes"]

    def obtener_horarios_formateados(self, horarios):
        f_horarios = ""
        for horario in horarios:
            f_horario = "dia:" + horario["dia"] + ","
            f_horario += "hora_desde:" + horario["hora_desde_reloj"] + ","
            f_horario += "hora_hasta:" + horario["hora_hasta_reloj"] + ";"
            f_horarios += f_horario

        return f_horarios[:-1]

    def se_encuentra_la_carrera(self, carrera, l_carreras):
        for l_carrera in l_carreras:
            if (carrera["id"] == l_carrera.carrera_id):
                return True
        return False

    def se_encuentra_el_horario(self, horario, l_horarios):
        for h_por_curso in l_horarios:
            l_horario = Horario.query.filter_by(id=h_por_curso.horario_id).first()
            if (horario["dia"].upper() == l_horario.dia and
                        horario["hora_desde"] == l_horario.hora_desde and
                        horario["hora_hasta"] == l_horario.hora_hasta):
                return True
        return False

    ##########################################################
    ##                      Tests                           ##
    ##########################################################

    def test_invocar_al_servicio_sin_estar_logueado(self):
        client = self.app.test_client()
        # response = client.post(MODIFICAR_CURSO_SERVICE)
        response = client.get(MODIFICAR_CURSO_SERVICE)
        assert (response.status_code == REDIRECTION_FOUND)


    def test_invocar_al_servicio_logueado_como_usuario(self):
        client = self.loguear_usuario()
        # response = client.post(MODIFICAR_CURSO_SERVICE)
        response = client.get(MODIFICAR_CURSO_SERVICE)
        assert (response.status_code == REDIRECTION_FOUND)


    def test_modificar_curso_una_carrera_con_todos_parametros_validos_lo_modifica(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas([self.CARRERA_1])
        parametros["primer_cuatrimestre"] = self.CURSO["se_dicta_primer_cuatrimestre"]
        parametros["segundo_cuatrimestre"] = self.CURSO["se_dicta_segundo_cuatrimestre"]
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        curso = Curso.query.filter_by(id=self.CURSO["id"]).first()

        assert (curso.id == self.CURSO["id"])

        carreras = CarreraPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(carreras) == 1)
        assert (self.se_encuentra_la_carrera(self.CARRERA_1, carreras))

        assert (curso.se_dicta_primer_cuatrimestre == self.CURSO["se_dicta_primer_cuatrimestre"])
        assert (curso.se_dicta_segundo_cuatrimestre == self.CURSO["se_dicta_segundo_cuatrimestre"])
        assert (curso.docentes == self.CURSO["docentes"])

        horarios = HorarioPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(horarios) == 2)
        for horario in self.CURSO["horarios"]:
            assert (self.se_encuentra_el_horario(horario, horarios))

    def test_modificar_curso_con_carreras_existentes_malos_separadores_da_error(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = "1:2"
        parametros["primer_cuatrimestre"] = self.CURSO["se_dicta_primer_cuatrimestre"]
        parametros["segundo_cuatrimestre"] = self.CURSO["se_dicta_segundo_cuatrimestre"]
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_modificar_curso_con_formato_valido_carreras_inexistentes_malos_separadores_da_error(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = "4;5"
        parametros["primer_cuatrimestre"] = self.CURSO["se_dicta_primer_cuatrimestre"]
        parametros["segundo_cuatrimestre"] = self.CURSO["se_dicta_segundo_cuatrimestre"]
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_modificar_curso_sin_enviar_parametro_carrera_da_error(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["primer_cuatrimestre"] = self.CURSO["se_dicta_primer_cuatrimestre"]
        parametros["segundo_cuatrimestre"] = self.CURSO["se_dicta_segundo_cuatrimestre"]
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_modificar_curso_con_parametro_carrera_vacio_da_error(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = ""
        parametros["primer_cuatrimestre"] = self.CURSO["se_dicta_primer_cuatrimestre"]
        parametros["segundo_cuatrimestre"] = self.CURSO["se_dicta_segundo_cuatrimestre"]
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_modificar_curso_con_parametro_carrera_invalido_da_error(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = "dasop99;902"
        parametros["primer_cuatrimestre"] = self.CURSO["se_dicta_primer_cuatrimestre"]
        parametros["segundo_cuatrimestre"] = self.CURSO["se_dicta_segundo_cuatrimestre"]
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_modificar_curso_dos_carreras_con_todos_parametros_validos_lo_modifica(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas([self.CARRERA_1, self.CARRERA_3])
        parametros["primer_cuatrimestre"] = self.CURSO["se_dicta_primer_cuatrimestre"]
        parametros["segundo_cuatrimestre"] = self.CURSO["se_dicta_segundo_cuatrimestre"]
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        curso = Curso.query.filter_by(id=self.CURSO["id"]).first()

        assert (curso.id == self.CURSO["id"])

        carreras = CarreraPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(carreras) == 2)
        assert (self.se_encuentra_la_carrera(self.CARRERA_1, carreras))
        assert (self.se_encuentra_la_carrera(self.CARRERA_3, carreras))

        assert (curso.se_dicta_primer_cuatrimestre == self.CURSO["se_dicta_primer_cuatrimestre"])
        assert (curso.se_dicta_segundo_cuatrimestre == self.CURSO["se_dicta_segundo_cuatrimestre"])
        assert (curso.docentes == self.CURSO["docentes"])

        horarios = HorarioPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(horarios) == 2)
        for horario in self.CURSO["horarios"]:
            assert (self.se_encuentra_el_horario(horario, horarios))

    def test_modificar_curso_se_dicta_solo_el_primer_cuatrimestre_lo_modifica(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = True
        parametros["segundo_cuatrimestre"] = False
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        curso = Curso.query.filter_by(id=self.CURSO["id"]).first()

        assert (curso.id == self.CURSO["id"])

        carreras = CarreraPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(carreras) == 2)
        assert (self.se_encuentra_la_carrera(self.CARRERA_1, carreras))
        assert (self.se_encuentra_la_carrera(self.CARRERA_2, carreras))

        assert (curso.se_dicta_primer_cuatrimestre == True)
        assert (curso.se_dicta_segundo_cuatrimestre == False)
        assert (curso.docentes == self.CURSO["docentes"])

        horarios = HorarioPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(horarios) == 2)
        for horario in self.CURSO["horarios"]:
            assert (self.se_encuentra_el_horario(horario, horarios))

    def test_modificar_curso_se_dicta_solo_el_segundo_cuatrimestre_lo_modifica(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = False
        parametros["segundo_cuatrimestre"] = True
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        curso = Curso.query.filter_by(id=self.CURSO["id"]).first()

        assert (curso.id == self.CURSO["id"])

        carreras = CarreraPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(carreras) == 2)
        assert (self.se_encuentra_la_carrera(self.CARRERA_1, carreras))
        assert (self.se_encuentra_la_carrera(self.CARRERA_2, carreras))

        assert (curso.se_dicta_primer_cuatrimestre == False)
        assert (curso.se_dicta_segundo_cuatrimestre == True)
        assert (curso.docentes == self.CURSO["docentes"])

        horarios = HorarioPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(horarios) == 2)
        for horario in self.CURSO["horarios"]:
            assert (self.se_encuentra_el_horario(horario, horarios))

    def test_modificar_curso_se_dicta_ambos_cuatrimestres_lo_modifica(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = True
        parametros["segundo_cuatrimestre"] = True
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        curso = Curso.query.filter_by(id=self.CURSO["id"]).first()

        assert (curso.id == self.CURSO["id"])

        carreras = CarreraPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(carreras) == 2)
        assert (self.se_encuentra_la_carrera(self.CARRERA_1, carreras))
        assert (self.se_encuentra_la_carrera(self.CARRERA_2, carreras))

        assert (curso.se_dicta_primer_cuatrimestre == True)
        assert (curso.se_dicta_segundo_cuatrimestre == True)
        assert (curso.docentes == self.CURSO["docentes"])

        horarios = HorarioPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(horarios) == 2)
        for horario in self.CURSO["horarios"]:
            assert (self.se_encuentra_el_horario(horario, horarios))

    def test_modificar_curso_no_se_dicta_ningun_cuatrimestre_lo_modifica(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = False
        parametros["segundo_cuatrimestre"] = False
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        curso = Curso.query.filter_by(id=self.CURSO["id"]).first()

        assert (curso.id == self.CURSO["id"])

        carreras = CarreraPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(carreras) == 2)
        assert (self.se_encuentra_la_carrera(self.CARRERA_1, carreras))
        assert (self.se_encuentra_la_carrera(self.CARRERA_2, carreras))

        assert (curso.se_dicta_primer_cuatrimestre == False)
        assert (curso.se_dicta_segundo_cuatrimestre == False)
        assert (curso.docentes == self.CURSO["docentes"])

        horarios = HorarioPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(horarios) == 2)
        for horario in self.CURSO["horarios"]:
            assert (self.se_encuentra_el_horario(horario, horarios))

    def test_modificar_curso_booleano_valores_se_dicta_primer_cuatrimestre_invalido_da_error(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = "Pepe"
        parametros["segundo_cuatrimestre"] = False
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_modificar_curso_no_se_envia_primer_cuatrimestre_invalido_da_error(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["segundo_cuatrimestre"] = False
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_modificar_curso_no_se_envia_segundo_cuatrimestre_invalido_da_error(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = True
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_modificar_curso_booleano_valores_se_dicta_segundo_cuatrimestre_invalido_da_error(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = True
        parametros["segundo_cuatrimestre"] = "90asdj"
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_modificar_curso_se_dicta_solo_el_primer_cuatrimestre_lo_modifica(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = True
        parametros["segundo_cuatrimestre"] = False
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        curso = Curso.query.filter_by(id=self.CURSO["id"]).first()

        assert (curso.id == self.CURSO["id"])

        carreras = CarreraPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(carreras) == 2)
        assert (self.se_encuentra_la_carrera(self.CARRERA_1, carreras))
        assert (self.se_encuentra_la_carrera(self.CARRERA_2, carreras))

        assert (curso.se_dicta_primer_cuatrimestre == True)
        assert (curso.se_dicta_segundo_cuatrimestre == False)
        assert (curso.docentes == self.CURSO["docentes"])

        horarios = HorarioPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(horarios) == 2)
        for horario in self.CURSO["horarios"]:
            assert (self.se_encuentra_el_horario(horario, horarios))

    def test_modificar_curso_se_dicta_solo_el_segundo_cuatrimestre_lo_modifica(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = False
        parametros["segundo_cuatrimestre"] = True
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        curso = Curso.query.filter_by(id=self.CURSO["id"]).first()

        assert (curso.id == self.CURSO["id"])

        carreras = CarreraPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(carreras) == 2)
        assert (self.se_encuentra_la_carrera(self.CARRERA_1, carreras))
        assert (self.se_encuentra_la_carrera(self.CARRERA_2, carreras))

        assert (curso.se_dicta_primer_cuatrimestre == False)
        assert (curso.se_dicta_segundo_cuatrimestre == True)
        assert (curso.docentes == self.CURSO["docentes"])

        horarios = HorarioPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(horarios) == 2)
        for horario in self.CURSO["horarios"]:
            assert (self.se_encuentra_el_horario(horario, horarios))

    def test_modificar_curso_se_dicta_ambos_cuatrimestres_lo_modifica(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = True
        parametros["segundo_cuatrimestre"] = True
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        curso = Curso.query.filter_by(id=self.CURSO["id"]).first()

        assert (curso.id == self.CURSO["id"])

        carreras = CarreraPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(carreras) == 2)
        assert (self.se_encuentra_la_carrera(self.CARRERA_1, carreras))
        assert (self.se_encuentra_la_carrera(self.CARRERA_2, carreras))

        assert (curso.se_dicta_primer_cuatrimestre == True)
        assert (curso.se_dicta_segundo_cuatrimestre == True)
        assert (curso.docentes == self.CURSO["docentes"])

        horarios = HorarioPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(horarios) == 2)
        for horario in self.CURSO["horarios"]:
            assert (self.se_encuentra_el_horario(horario, horarios))

    def test_modificar_curso_no_se_dicta_ningun_cuatrimestre_lo_modifica(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = False
        parametros["segundo_cuatrimestre"] = False
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        curso = Curso.query.filter_by(id=self.CURSO["id"]).first()

        assert (curso.id == self.CURSO["id"])

        carreras = CarreraPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(carreras) == 2)
        assert (self.se_encuentra_la_carrera(self.CARRERA_1, carreras))
        assert (self.se_encuentra_la_carrera(self.CARRERA_2, carreras))

        assert (curso.se_dicta_primer_cuatrimestre == False)
        assert (curso.se_dicta_segundo_cuatrimestre == False)
        assert (curso.docentes == self.CURSO["docentes"])

        horarios = HorarioPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(horarios) == 2)
        for horario in self.CURSO["horarios"]:
            assert (self.se_encuentra_el_horario(horario, horarios))

    def test_modificar_curso_se_dicta_solo_el_primer_cuatrimestre_con_texto_booleano_lo_modifica(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = 'true'
        parametros["segundo_cuatrimestre"] = 'false'
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        curso = Curso.query.filter_by(id=self.CURSO["id"]).first()

        assert (curso.id == self.CURSO["id"])

        carreras = CarreraPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(carreras) == 2)
        assert (self.se_encuentra_la_carrera(self.CARRERA_1, carreras))
        assert (self.se_encuentra_la_carrera(self.CARRERA_2, carreras))

        assert (curso.se_dicta_primer_cuatrimestre == True)
        assert (curso.se_dicta_segundo_cuatrimestre == False)
        assert (curso.docentes == self.CURSO["docentes"])

        horarios = HorarioPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(horarios) == 2)
        for horario in self.CURSO["horarios"]:
            assert (self.se_encuentra_el_horario(horario, horarios))

    def test_modificar_curso_se_dicta_solo_el_segundo_cuatrimestre_con_texto_booleano_lo_modifica(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = 'false'
        parametros["segundo_cuatrimestre"] = 'true'
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        curso = Curso.query.filter_by(id=self.CURSO["id"]).first()

        assert (curso.id == self.CURSO["id"])

        carreras = CarreraPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(carreras) == 2)
        assert (self.se_encuentra_la_carrera(self.CARRERA_1, carreras))
        assert (self.se_encuentra_la_carrera(self.CARRERA_2, carreras))

        assert (curso.se_dicta_primer_cuatrimestre == False)
        assert (curso.se_dicta_segundo_cuatrimestre == True)
        assert (curso.docentes == self.CURSO["docentes"])

        horarios = HorarioPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(horarios) == 2)
        for horario in self.CURSO["horarios"]:
            assert (self.se_encuentra_el_horario(horario, horarios))

    def test_modificar_curso_se_dicta_ambos_cuatrimestres_con_texto_booleano_lo_modifica(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = 'true'
        parametros["segundo_cuatrimestre"] = 'true'
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        curso = Curso.query.filter_by(id=self.CURSO["id"]).first()

        assert (curso.id == self.CURSO["id"])

        carreras = CarreraPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(carreras) == 2)
        assert (self.se_encuentra_la_carrera(self.CARRERA_1, carreras))
        assert (self.se_encuentra_la_carrera(self.CARRERA_2, carreras))

        assert (curso.se_dicta_primer_cuatrimestre == True)
        assert (curso.se_dicta_segundo_cuatrimestre == True)
        assert (curso.docentes == self.CURSO["docentes"])

        horarios = HorarioPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(horarios) == 2)
        for horario in self.CURSO["horarios"]:
            assert (self.se_encuentra_el_horario(horario, horarios))

    def test_modificar_curso_no_se_dicta_ningun_cuatrimestre_con_texto_booleano_lo_modifica(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = 'false'
        parametros["segundo_cuatrimestre"] = 'false'
        parametros["docentes"] = self.obtener_docentes_formateados(self.CURSO)
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        curso = Curso.query.filter_by(id=self.CURSO["id"]).first()

        assert (curso.id == self.CURSO["id"])

        carreras = CarreraPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(carreras) == 2)
        assert (self.se_encuentra_la_carrera(self.CARRERA_1, carreras))
        assert (self.se_encuentra_la_carrera(self.CARRERA_2, carreras))

        assert (curso.se_dicta_primer_cuatrimestre == False)
        assert (curso.se_dicta_segundo_cuatrimestre == False)
        assert (curso.docentes == self.CURSO["docentes"])

        horarios = HorarioPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(horarios) == 2)
        for horario in self.CURSO["horarios"]:
            assert (self.se_encuentra_el_horario(horario, horarios))

    def test_modificar_curso_docentes_lo_modifica(self):
        NUEVOS_DOCENTES = "Docentes1,docentes3 - docentes& Mryy"

        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = self.CURSO["se_dicta_primer_cuatrimestre"]
        parametros["segundo_cuatrimestre"] = self.CURSO["se_dicta_segundo_cuatrimestre"]
        parametros["docentes"] = NUEVOS_DOCENTES
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        curso = Curso.query.filter_by(id=self.CURSO["id"]).first()

        assert (curso.id == self.CURSO["id"])

        carreras = CarreraPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(carreras) == 2)
        assert (self.se_encuentra_la_carrera(self.CARRERA_1, carreras))
        assert (self.se_encuentra_la_carrera(self.CARRERA_2, carreras))

        assert (curso.se_dicta_primer_cuatrimestre == self.CURSO["se_dicta_primer_cuatrimestre"])
        assert (curso.se_dicta_segundo_cuatrimestre == self.CURSO["se_dicta_segundo_cuatrimestre"])
        assert (curso.docentes == NUEVOS_DOCENTES)

        horarios = HorarioPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(horarios) == 2)
        for horario in self.CURSO["horarios"]:
            assert (self.se_encuentra_el_horario(horario, horarios))

    def test_modificar_curso_no_enviar_docentes_da_error(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = 'false'
        parametros["segundo_cuatrimestre"] = 'false'
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_modificar_horarios_validos_agregar_un_horario_nuevo_lo_modifica(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = self.CURSO["se_dicta_primer_cuatrimestre"]
        parametros["segundo_cuatrimestre"] = self.CURSO["se_dicta_segundo_cuatrimestre"]
        parametros["docentes"] = self.CURSO["docentes"]
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"] + [self.HORARIO_3])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        curso = Curso.query.filter_by(id=self.CURSO["id"]).first()

        assert (curso.id == self.CURSO["id"])

        carreras = CarreraPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(carreras) == 2)
        assert (self.se_encuentra_la_carrera(self.CARRERA_1, carreras))
        assert (self.se_encuentra_la_carrera(self.CARRERA_2, carreras))

        assert (curso.se_dicta_primer_cuatrimestre == self.CURSO["se_dicta_primer_cuatrimestre"])
        assert (curso.se_dicta_segundo_cuatrimestre == self.CURSO["se_dicta_segundo_cuatrimestre"])
        assert (curso.docentes == self.CURSO["docentes"])

        horarios = HorarioPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(horarios) == 3)
        for horario in (self.CURSO["horarios"] + [self.HORARIO_3]):
            assert (self.se_encuentra_el_horario(horario, horarios))

    def test_modificar_horarios_validos_solo_horarios_nuevos_lo_modifica(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = self.CURSO["se_dicta_primer_cuatrimestre"]
        parametros["segundo_cuatrimestre"] = self.CURSO["se_dicta_segundo_cuatrimestre"]
        parametros["docentes"] = self.CURSO["docentes"]
        parametros["horarios"] = self.obtener_horarios_formateados([self.HORARIO_3, self.HORARIO_4])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == SUCCESS_OK)

        curso = Curso.query.filter_by(id=self.CURSO["id"]).first()

        assert (curso.id == self.CURSO["id"])

        carreras = CarreraPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(carreras) == 2)
        assert (self.se_encuentra_la_carrera(self.CARRERA_1, carreras))
        assert (self.se_encuentra_la_carrera(self.CARRERA_2, carreras))

        assert (curso.se_dicta_primer_cuatrimestre == self.CURSO["se_dicta_primer_cuatrimestre"])
        assert (curso.se_dicta_segundo_cuatrimestre == self.CURSO["se_dicta_segundo_cuatrimestre"])
        assert (curso.docentes == self.CURSO["docentes"])

        horarios = HorarioPorCurso.query.filter_by(curso_id=self.CURSO["id"]).all()
        assert (len(horarios) == 2)
        for horario in [self.HORARIO_3, self.HORARIO_4]:
            assert (self.se_encuentra_el_horario(horario, horarios))

    def test_modificar_curso_horario_invalido_da_error(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = self.CURSO["se_dicta_primer_cuatrimestre"]
        parametros["segundo_cuatrimestre"] = self.CURSO["se_dicta_segundo_cuatrimestre"]
        parametros["docentes"] = self.CURSO["docentes"]
        parametros["horarios"] = "sd54fs5"

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_modificar_curso_no_enviar_horario_da_error(self):
        parametros = {}
        parametros["id_curso"] = self.CURSO["id"]
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = self.CURSO["se_dicta_primer_cuatrimestre"]
        parametros["segundo_cuatrimestre"] = self.CURSO["se_dicta_segundo_cuatrimestre"]
        parametros["docentes"] = self.CURSO["docentes"]

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_modificar_curso_no_enviar_id_curso_da_error(self):
        parametros = {}
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = self.CURSO["se_dicta_primer_cuatrimestre"]
        parametros["segundo_cuatrimestre"] = self.CURSO["se_dicta_segundo_cuatrimestre"]
        parametros["docentes"] = self.CURSO["docentes"]
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_modificar_curso_id_curso_invalido_da_error(self):
        parametros = {}
        parametros["id_curso"] = "sd9"
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = self.CURSO["se_dicta_primer_cuatrimestre"]
        parametros["segundo_cuatrimestre"] = self.CURSO["se_dicta_segundo_cuatrimestre"]
        parametros["docentes"] = self.CURSO["docentes"]
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)

    def test_modificar_curso_id_curso_valido_inexistente_da_error(self):
        parametros = {}
        parametros["id_curso"] = "15"
        parametros["carreras"] = self.obtener_carreras_formateadas(self.CURSO["carreras"])
        parametros["primer_cuatrimestre"] = self.CURSO["se_dicta_primer_cuatrimestre"]
        parametros["segundo_cuatrimestre"] = self.CURSO["se_dicta_segundo_cuatrimestre"]
        parametros["docentes"] = self.CURSO["docentes"]
        parametros["horarios"] = self.obtener_horarios_formateados(self.CURSO["horarios"])

        client = self.loguear_administrador()
        # response = client.post(MODIFICAR_CURSO_SERVICE, data=parametros)
        response = client.get(MODIFICAR_CURSO_SERVICE, query_string=parametros)
        assert (response.status_code == CLIENT_ERROR_BAD_REQUEST)


if __name__ == '__main__':
    import unittest

    unittest.main()
