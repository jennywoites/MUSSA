def get_str_cuatrimestre(cuatrimestre):
    if cuatrimestre < 10:
        return "0" + str(cuatrimestre)
    return str(cuatrimestre)


def es_par(num):
    return num % 2 == 0


def es_horario_valido_para_el_cuatrimestre(parametros, curso, cuatrimestre):
    if parametros.primer_cuatrimestre_es_impar:
        if not es_par(cuatrimestre): #Es un primer cuatrimestre del anio
            return curso.se_dicta_primer_cuatrimestre

        return curso.se_dicta_segundo_cuatrimestre

    if not es_par(cuatrimestre): #Es un segundo cuatrimestre del anio
        return curso.se_dicta_segundo_cuatrimestre

    return curso.se_dicta_primer_cuatrimestre
