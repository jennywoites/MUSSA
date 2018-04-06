import hashlib


class Horario:
    def inicializar_con_JSON(self, datos_json):
        self.dia = datos_json["dia"]
        self.hora_inicio = float(datos_json["hora_inicio"])
        self.hora_fin = float(datos_json["hora_fin"])

    def __init__(self, dia='', hora_inicio='', hora_fin='', datos_JSON=''):
        """
        Hora_inicio, Hora_fin: Numeros enteros si son horas en punto. Decimales, ejemplo 7.5 si son las 07:30
        """
        if datos_JSON:
            return self.inicializar_con_JSON(datos_JSON)

        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin

    def __lt__(self, otro):
        if self.dia == otro.dia:
            if self.hora_inicio == otro.hora_inicio:
                return self.hora_fin < otro.hora_fin
            return self.hora_inicio < otro.hora_inicio
        return self.dia < otro.dia

    def __eq__(self, otro):
        return (self.dia == otro.dia and
                self.hora_inicio == otro.hora_inicio and
                self.hora_fin == self.hora_fin)

    def __str__(self):
        SALTO = "\n"
        horario = "{" + SALTO
        horario += "dia: " + str(self.dia) + SALTO
        horario += "hora_inicio: " + str(self.hora_inicio) + SALTO
        horario += "hora_fin: " + str(self.hora_fin) + SALTO
        horario += "}" + SALTO
        return horario

    def obtener_hash_horario(self):
        horario = str(self)
        return hashlib.sha1(horario.encode('utf-8'))

    def generar_JSON(self):
        return {
            "dia": self.dia,
            "hora_inicio": self.hora_inicio,
            "hora_fin": self.hora_fin
        }

    def convertir_a_franja(self, hora):
        base = 1
        hora_origen = 7
        if (round(hora) != hora):
            base += 1
            hora = int(hora - 0.5)
        return int((hora - hora_origen) * 2 + base)

    def convertir_franja_a_hora(self, franja):
        hora_origen = 7
        return hora_origen + 0.5 * (franja - 1)

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
