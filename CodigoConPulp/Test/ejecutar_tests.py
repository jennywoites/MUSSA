from Test_minimiza_franjas_libres_en_seleccion_de_curso_con_unico_resultado_menor_posible import Test_minimiza_franjas_libres_en_seleccion_de_curso_con_unico_resultado_menor_posible
from Test_minimiza_franjas_libres_en_seleccion_de_curso_con_dos_posibles_resultados import Test_minimiza_franjas_libres_en_seleccion_de_curso_con_dos_posibles_resultados
from Test_correlatividades_se_hacen_en_orden import Test_correlatividades_se_hacen_en_orden
from Test_correlatividades_se_hacen_en_orden_varios_niveles_correlatividades import Test_correlatividades_se_hacen_en_orden_varios_niveles_correlatividades


def tests_a_ejecutar():
    tests = []
    tests.append(Test_minimiza_franjas_libres_en_seleccion_de_curso_con_unico_resultado_menor_posible())
    tests.append(Test_minimiza_franjas_libres_en_seleccion_de_curso_con_dos_posibles_resultados())
    tests.append(Test_correlatividades_se_hacen_en_orden())
    tests.append(Test_correlatividades_se_hacen_en_orden_varios_niveles_correlatividades())
    return tests


def ejecutar_todos():
    print("Esta accion puede demorar varios minutos...")

    tests = tests_a_ejecutar()
    for test_a_ejecutar in tests:
        print("Ejecutando: " + test_a_ejecutar.get_nombre_test())
        test_a_ejecutar.ejecutar_test()
        print("Se termino de ejecutar el test correctamente")

    print("Todos los test se ejecutaron exitosamente!")


if __name__ == "__main__":
    ejecutar_todos()