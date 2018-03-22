if __name__ == '__main__':
    import sys

    sys.path.append("../..")

from tests.TestAPIServicios.TestBase import TestBase
import os
import json
from app import db
from app.models.alumno_models import Alumno
from app.models.plan_de_estudios_models import EstadoPlanDeEstudios, PlanDeEstudios
from datetime import datetime
from app.DAO.PlanDeCarreraDAO import PLAN_EN_CURSO
from app.API_Rest.GeneradorPlanCarreras.my_utils import get_str_fecha_y_hora_actual
from AsyncTasks.broker_generador_greedy import tarea_generar_plan_greedy


class TestEstadisticasGeneracionPlanDeEstudios(TestBase):
    ##########################################################
    ##                   Configuracion                      ##
    ##########################################################

    def get_test_name(self):
        return "test_estadisticas_generacion_plan_de_estudios"

    def crear_datos_bd(self):
        alumno = Alumno(user_id=self.get_usuario().id)
        db.session.add(alumno)
        db.session.commit()

    ##########################################################
    ##                      Tests                           ##
    ##########################################################

    def test_ejecutar_diferentes_pedidos_de_generacion_de_planes_de_estudios(self):
        archivos_parametros, archivos_estadisticas = self.obtener_rutas_de_archivos()
        for numero_prueba in archivos_parametros:
            if not numero_prueba in archivos_estadisticas:
                continue

            parametros = None
            estadisticas = None
            with open(archivos_parametros[numero_prueba], 'r') as file:
                parametros = json.loads(file.read())

            with open(archivos_estadisticas[numero_prueba], 'r') as file:
                estadisticas = json.loads(file.read())

            self.invocar_servicios_generacion_plan(parametros, estadisticas)

    def invocar_servicios_generacion_plan(self, parametros, estadisticas):
        self.generar_plan_de_estudios(parametros)

        estadisticas["tipo_solicitud"] = "Testing"
        estadisticas["fecha_solicitado"] = get_str_fecha_y_hora_actual()

        self.invocar_servicio_generacion_plan_greedy(parametros, estadisticas)
        self.invocar_servicio_generacion_plan_ple(parametros, estadisticas)

    def invocar_servicio_generacion_plan_greedy(self, parametros, estadisticas):
        estadisticas["algoritmo"] = "GREEDY"
        tarea = tarea_generar_plan_greedy.delay(parametros, estadisticas)
        assert (tarea is not None)

    def invocar_servicio_generacion_plan_ple(self, parametros, estadisticas):
        estadisticas["algoritmo"] = "PLE"
        # FIXME: Hacer la invocacion del servicio

    def generar_plan_de_estudios(self, parametros):
        estado_en_curso = EstadoPlanDeEstudios.query.filter_by(numero=PLAN_EN_CURSO).first()

        plan_de_estudios = PlanDeEstudios(
            alumno_id=Alumno.query.filter_by(user_id=self.get_usuario().id).first().id,
            fecha_generacion=datetime.today(),
            fecha_ultima_actualizacion=datetime.today(),
            estado_id=estado_en_curso.id,
            cuatrimestre_inicio_plan=parametros["cuatrimestre_inicio"],
            anio_inicio_plan=parametros["anio_inicio"]
        )
        db.session.add(plan_de_estudios)
        db.session.commit()

        parametros["user_id"] = self.get_usuario().id
        parametros["id_plan_estudios"] = plan_de_estudios.id

    def obtener_rutas_de_archivos(self):
        ruta_archivo = os.path.join(os.getcwd(), 'DatosEstadisticas')
        archivos_parametros = {}
        archivos_estadisticas = {}
        for ruta in os.listdir(ruta_archivo):
            numero, tipo = ruta.split("_")
            if tipo == "parametros":
                archivos_parametros[numero] = os.path.join('DatosEstadisticas', ruta)
            elif tipo == "estadisticas":
                archivos_estadisticas[numero] = os.path.join('DatosEstadisticas', ruta)
        return archivos_parametros, archivos_estadisticas


if __name__ == '__main__':
    import unittest

    unittest.main()
