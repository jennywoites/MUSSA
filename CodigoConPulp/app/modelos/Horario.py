
class Horario:
    
    def __init__(self, dia, hora_inicio, hora_fin):
        """
        Hora_inicio, Hora_fin: Numeros enteros si son horas en punto. Decimales, ejemplo 7.5 si son las 07:30
        """
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin

    def convertir_a_franja(self, hora):
        base = 1
        hora_origen = 7
        if (round(hora) != hora):
            base += 1
            hora = int(hora - 0.5)
        return (hora - hora_origen)*2 + base

    def get_franjas_utilizadas(self):
        """
        Las franjas horarias van cada media hora desde las 7am hasta las 23:30
        07:00 a 07:30 --> 1
        07:30 a 08:00 --> 2
        08:00 a 08:30 --> 3
        ...
        Devuelve una lista con los numeros de las franjas horarias desde hora_inicio hasta hora_fin
        """
        franja_inicio = self.convertir_a_franja(self.hora_inicio)
        franja_final = self.convertir_a_franja(self.hora_fin)
        return [x for x in range(franja_inicio, franja_final)]

    def __str__(self):
        return "Horario: {} - Desde: {} A: {}".format(self.dia, self.hora_inicio, self.hora_fin)
