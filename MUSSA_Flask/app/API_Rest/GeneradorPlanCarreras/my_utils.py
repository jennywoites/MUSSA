def get_str_cuatrimestre(cuatrimestre):
    if cuatrimestre < 10:
        return "0" + str(cuatrimestre)
    return str(cuatrimestre)