import os
import sys
sys.path.append("../..")

from tests.TestResolucionPlanDeEstudios.Test_minimiza_franjas_libres_en_seleccion_de_curso_con_unico_resultado_menor_posible import Test_minimiza_franjas_libres_en_seleccion_de_curso_con_unico_resultado_menor_posible
from tests.TestResolucionPlanDeEstudios.Test_minimiza_franjas_libres_en_seleccion_de_curso_con_dos_posibles_resultados import Test_minimiza_franjas_libres_en_seleccion_de_curso_con_dos_posibles_resultados
from tests.TestResolucionPlanDeEstudios.Test_correlatividades_se_hacen_en_orden import Test_correlatividades_se_hacen_en_orden
from tests.TestResolucionPlanDeEstudios.Test_correlatividades_se_hacen_en_orden_varios_niveles_correlatividades import Test_correlatividades_se_hacen_en_orden_varios_niveles_correlatividades
from tests.TestResolucionPlanDeEstudios.Test_creditos_minimos_para_cursar import Test_creditos_minimos_para_cursar
from tests.TestResolucionPlanDeEstudios.Test_plan_licenciatura_con_unico_horario_por_materia_no_superpuestos import Test_plan_licenciatura_con_unico_horario_por_materia_no_superpuestos
from tests.TestResolucionPlanDeEstudios.Test_plan_licenciatura_con_unico_horario_por_materia_no_superpuestos_con_materias_electivas import Test_plan_licenciatura_con_unico_horario_por_materia_no_superpuestos_con_materias_electivas
from tests.TestResolucionPlanDeEstudios.Test_plan_licenciatura_completo_con_unico_horario_por_materia_no_superpuestos import Test_plan_licenciatura_completo_con_unico_horario_por_materia_no_superpuestos
from tests.TestResolucionPlanDeEstudios.Test_plan_licenciatura_con_horarios_cargados_desde_pdf_fiuba import Test_plan_licenciatura_con_horarios_cargados_desde_pdf_fiuba

def tests_a_ejecutar():
    tests = []
    #tests.append(Test_minimiza_franjas_libres_en_seleccion_de_curso_con_unico_resultado_menor_posible())
    #tests.append(Test_minimiza_franjas_libres_en_seleccion_de_curso_con_dos_posibles_resultados())
    tests.append(Test_correlatividades_se_hacen_en_orden())
    tests.append(Test_correlatividades_se_hacen_en_orden_varios_niveles_correlatividades())
    tests.append(Test_creditos_minimos_para_cursar())
    tests.append(Test_plan_licenciatura_con_unico_horario_por_materia_no_superpuestos())
    tests.append(Test_plan_licenciatura_con_unico_horario_por_materia_no_superpuestos_con_materias_electivas())
    tests.append(Test_plan_licenciatura_completo_con_unico_horario_por_materia_no_superpuestos())
    tests.append(Test_plan_licenciatura_con_horarios_cargados_desde_pdf_fiuba())
    return tests


def limpiar_o_crear_directorio():
    ruta = "resultados_tests"
    if not os.path.exists(ruta):
        os.system('mkdir {}'.format(ruta))
    else:
        os.system('find {} -type f -delete'.format(ruta))


def ejecutar_todos():
    print("Esta accion puede demorar varios minutos...")

    limpiar_o_crear_directorio()

    tests = tests_a_ejecutar()
    for test_a_ejecutar in tests:
        print("Ejecutando: " + test_a_ejecutar.get_nombre_test())
        test_a_ejecutar.ejecutar_test()
        print("Se termino de ejecutar el test correctamente")

    print("Todos los test se ejecutaron exitosamente!")


if __name__ == "__main__":
    ejecutar_todos()