from datetime import datetime
import os
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import functools
from app.models.user_models import User
from app.models.alumno_models import AlumnosCarreras
from app.models.carreras_models import Carrera
from app.DAO.MateriasDAO import APROBADA, DESAPROBADA, FINAL_PENDIENTE, EN_CURSO
from app.models.generadorJSON.alumno_generadorJSON import generarJSON_materia_alumno
from app.models.filtros.alumno_filter import filtrar_materias_alumno
from app.API_Rest.Services.AlumnoServices.AllMateriasAlumnoService import cmp_materias_result

SALTO_DE_LINEA = "<br />"


class GeneradorPDF:
    def __init__(self, ruta):
        self.pagesize = A4
        self.leftmargin = 72
        self.rightmargin = 72
        self.doc = SimpleDocTemplate(
            ruta,
            pagesize=self.pagesize,
            rightMargin=self.rightmargin,
            leftMargin=self.leftmargin,
            topMargin=20,
            bottomMargin=18
        )
        self.story = []
        self.estilos = self.generar_estilos()

    def generar_estilos(self):
        estilos = getSampleStyleSheet()
        estilos.add(ParagraphStyle(name='Justificado', alignment=TA_JUSTIFY, fontSize=12, leading=18))
        estilos.add(ParagraphStyle(name='Justificado_Very_Small', alignment=TA_JUSTIFY, fontSize=8, leading=18))
        estilos.add(ParagraphStyle(name='Justificado_identado', alignment=TA_JUSTIFY, fontSize=12, leading=18, firstLineIndent=100))
        estilos.add(ParagraphStyle(name='Alinear_Derecha', alignment=TA_RIGHT, fontSize=12))
        estilos.add(ParagraphStyle(name='Alinear_Derecha_con_sangria', alignment=TA_LEFT, fontSize=12, firstLineIndent=110))
        estilos.add(
            ParagraphStyle(name='Alinear_Derecha_Bold', alignment=TA_RIGHT, fontSize=12, fontName='Helvetica-Bold'))
        estilos.add(ParagraphStyle(name='Alinear_Derecha_Small', alignment=TA_RIGHT, fontSize=8))
        estilos.add(ParagraphStyle(name='Alinear_Izquierda', alignment=TA_LEFT, fontSize=12))
        estilos.add(ParagraphStyle(name='Alinear_Izquierda_Small', alignment=TA_LEFT, fontSize=10))
        estilos.add(ParagraphStyle(name='Alinear_Izquierda_con_sangria', alignment=TA_LEFT, fontSize=12, firstLineIndent=60))
        estilos.add(
            ParagraphStyle(name='Alinear_Izquierda_Bold', alignment=TA_LEFT, fontSize=12, fontName='Helvetica-Bold'))
        estilos.add(ParagraphStyle(name='Centrado', alignment=TA_CENTER, fontSize=12))
        estilos.add(ParagraphStyle(name='Centrado_Small', alignment=TA_CENTER, fontSize=10))
        estilos.add(ParagraphStyle(name='Bullet_Grande', alignment=TA_JUSTIFY, fontSize=11, fontName='Helvetica',
                                   bulletFontName='Helvetica', bulletFontSize=11, bulletIndent=35))
        return estilos

    def insertar_logos(self):
        logo_uba = os.path.join('app', 'static', 'images', 'logo_uba.png')
        logo_fiuba = os.path.join('app', 'static', 'images', 'logo_fiuba.png')

        tbl_data = [[
            Image(logo_uba, 1 * inch * 1.5, 0.65 * inch * 1.5, hAlign='LEFT'),
            Image(logo_fiuba, 1.5 * inch, 0.5 * inch, hAlign='RIGTH')
        ]]

        ancho_columna = (self.pagesize[0] - self.leftmargin - self.rightmargin) / 2
        tbl = Table(tbl_data,  colWidths=ancho_columna)
        tbl.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        self.story.append(tbl)

        self.story.append(Spacer(1, 12))
        self.story.append(Spacer(1, 12))

    def insertar_fecha_en_buenos_aires(self):
        lugar = "Buenos Aires, "
        hoy = datetime.today()

        MESES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
                 'Agosto', 'Setiembre', 'Octubre', 'Noviembre', 'Diciembre']
        fecha = "{} de {} de {}".format(hoy.day, MESES[hoy.month - 1], hoy.year)

        self.story.append(Paragraph(lugar + fecha, self.estilos["Alinear_Derecha"]))
        self.story.append(Spacer(1, 12))

    def insertar_datos_direccion_alumnos(self):
        self.story.append(Paragraph("Secretaría Académica", self.estilos["Alinear_Derecha_Small"]))
        self.story.append(Paragraph("Dirección de Alumnos de Grado", self.estilos["Alinear_Derecha_Small"]))
        self.story.append(Spacer(1, 12))

    def insertar_objeto(self, texto_objeto):
        texto = self.dividir_texto_en_lineas_de_longitud_maxima("OBJETO: " + texto_objeto, 35)
        self.story.append(Paragraph(texto, self.estilos["Alinear_Derecha_Bold"]))
        self.story.append(Spacer(3, 12))

    def dividir_texto_en_lineas_de_longitud_maxima(self, texto_origen, longitud_maxima):
        texto = ""
        dividido = 0
        for palabra in texto_origen.split(" "):
            if ((len(texto + " " + palabra) - len(SALTO_DE_LINEA) * dividido) // longitud_maxima) - dividido > 0:
                texto += SALTO_DE_LINEA
                dividido += 1
            texto += " " + palabra
        return texto

    def insertar_dirigida_al_decano(self):
        self.story.append(Paragraph("Señor Decano de la", self.estilos["Alinear_Izquierda_Bold"]))
        self.story.append(Paragraph("Facultad de Ingeniería:", self.estilos["Alinear_Izquierda"]))
        self.story.append(Spacer(1, 12))

    def insertar_datos_alumnos_y_motivo(self, alumno, motivo):
        usuario = User.query.get(alumno.user_id)

        texto = "Quien suscribe, " + usuario.first_name + " " + usuario.last_name + ", "
        texto += "legajo Nº " + alumno.get_padron() + " estudiante de " + self.obtener_texto_carreras(alumno)
        texto += " tiene el agrado de dirigirse a Usted con el fin de solicitarle " + motivo + "."

        self.story.append(Paragraph(texto, self.estilos["Justificado_identado"]))
        self.story.append(Spacer(1, 12))

    def insertar_datos_alumno(self, alumno):
        usuario = User.query.get(alumno.user_id)

        texto = usuario.last_name + ", " + usuario.last_name + SALTO_DE_LINEA
        texto += "Padrón: " + alumno.get_padron()

        self.story.append(Paragraph(texto, self.estilos["Justificado"]))
        self.story.append(Spacer(1, 12))

    def obtener_texto_carreras(self, alumno):
        carreras = []
        for dato in AlumnosCarreras.query.filter_by(alumno_id=alumno.id).all():
            carreras.append(Carrera.query.get(dato.carrera_id))

        if len(carreras) == 0:
            return "ninguna carrera"

        texto_carreras = "la carrera" if len(carreras) == 1 else "las carreras"
        for i in range(len(carreras)):
            carrera = carreras[i]
            separador = " y " if (i == len(carreras) - 2) else ", "
            texto_carreras += " " + carrera.get_descripcion_carrera() + separador
        return texto_carreras[:-2]

    def insertar_informacion_adjunta(self):
        self.story.append(Paragraph("ADJUNTO LA SIGUIENTE INFORMACIÓN:", self.estilos["Alinear_Izquierda_Bold"]))
        self.story.append(Spacer(1, 12))

        bullet = '<bullet>&bull;</bullet>'

        nota = "Nota ampliando detalladamente los motivos de la presente solicitud (en caso de ser necesario)"
        self.story.append(Paragraph(bullet + nota, self.estilos["Bullet_Grande"]))
        self.story.append(Spacer(1, 10))

        lista_aprobadas = "Listado de asignaturas aprobadas con código, nombre, libro, folio, fecha y calificación"
        self.story.append(Paragraph(bullet + lista_aprobadas, self.estilos["Bullet_Grande"]))
        self.story.append(Spacer(1, 10))

        lista_cursando = "Listado de asignaturas que curso actualmente"
        self.story.append(Paragraph(bullet + lista_cursando, self.estilos["Bullet_Grande"]))
        self.story.append(Spacer(1, 10))
        self.story.append(Spacer(1, 12))

    def insertar_despedida_formal(self):
        texto = "Sin otro particular, saludo al Sr. Decano con la más distinguida consideración."
        self.story.append(Paragraph(texto, self.estilos["Justificado_identado"]))
        self.story.append(Spacer(1, 12))

    def insertar_firma_y_aclaracion(self):
        self.story.append(Spacer(1, 12))
        self.story.append(Spacer(1, 12))
        self.story.append(Spacer(1, 12))

        puntuaciones = "............................................."
        tbl_data = [
            [
                Paragraph(puntuaciones, self.estilos["Alinear_Izquierda"]),
                Paragraph(puntuaciones, self.estilos["Alinear_Derecha"])
            ],
            [
                Paragraph("Firma", self.estilos["Alinear_Izquierda_con_sangria"]),
                Paragraph("Aclaración", self.estilos["Alinear_Derecha_con_sangria"])
            ]
        ]
        tbl = Table(tbl_data)
        self.story.append(tbl)

        self.story.append(Spacer(1, 12))
        self.story.append(Spacer(1, 12))
        self.story.append(Spacer(1, 12))

    def insertar_informacion_contacto_alumno(self, alumno, telefono, domicilio, localidad, dni, anio_ingreso):
        usuario = User.query.get(alumno.user_id)

        texto = "Teléfono / Celular: " + telefono + ", "
        texto += "Domicilio: " + domicilio + ", "
        texto += "Localidad: " + localidad + SALTO_DE_LINEA
        texto += "DNI: " + dni + ", "
        texto += "Año de Ingreso a la Facultad de Ingeniería: " + anio_ingreso + SALTO_DE_LINEA
        texto += "E-mail: " + usuario.email

        self.story.append(Paragraph(texto, self.estilos["Justificado"]))
        self.story.append(Spacer(1, 12))

    def insertar_informacion_tramite(self):
        texto = "Información importante para el alumno: Para concluir el trámite, el/la alumno/a recibirá mediante " \
                "correo electrónico la Resolución del mismo. El/La interesado/a deberá confirmar dicha recepción (vía " \
                "correo electrónico). Horarios y días de Atención de Ventanilla de Alumnos: Lunes a Viernes de 9 a " \
                "12:30 y 15:30 a 19 hs."
        self.story.append(Paragraph(texto, self.estilos["Justificado_Very_Small"]))
        self.story.append(Spacer(1, 12))

    def insertar_info_depto_alumnos(self):
        texto = "DIRECCIÓN DE ALUMNOS DE GRADO" + SALTO_DE_LINEA
        texto += "Tel +54 (11) 52850569/ 50570 / 50568 / 50566" + SALTO_DE_LINEA
        texto += "Av. Paseo Colon 850 - P.B. / Ciudad de Buenos Aires, Argentina" + SALTO_DE_LINEA
        texto += "www.fi.uba.ar - dalumnos@fi.uba.ar" + SALTO_DE_LINEA

        self.story.append(Paragraph(texto, self.estilos["Centrado_Small"]))

    def insertar_salto_de_pagina(self):
        self.story.append(PageBreak())

    def insertar_nota_extendida(self, nota):
        texto = "Nota extendiendo el motivo de la solicitud:"
        self.story.append(Paragraph(texto, self.estilos["Alinear_Izquierda_Bold"]))
        self.story.append(Spacer(1, 12))

        self.story.append(Paragraph(nota, self.estilos["Justificado_identado"]))
        self.story.append(Spacer(1, 12))

    def insertar_materias_rendidas(self, alumno, carreras_filtradas=[]):
        self.insertar_materias_por_carrera(
            "Materias Rendidas",
            'Sin materias aprobadas / desaprobadas para esta carrera',
            alumno,
            [APROBADA, DESAPROBADA],
            carreras_filtradas
        )
        self.story.append(Spacer(1, 12))

    def insertar_materias_final_pendiente(self, alumno, carreras_filtradas=[]):
        self.insertar_materias_por_carrera(
            "Materias con final pendiente",
            'No hay materias con final pendiente para esta carrera',
            alumno,
            [FINAL_PENDIENTE],
            carreras_filtradas
        )
        self.story.append(Spacer(1, 12))

    def insertar_materias_en_curso(self, alumno, carreras_filtradas=[]):
        self.insertar_materias_por_carrera(
            "Cursando este cuatrimestre",
            'No se cursan materias de esta carrera este cuatrimestre',
            alumno,
            [EN_CURSO],
            carreras_filtradas
        )

    def insertar_materias_por_carrera(self, titulo, texto_sin_datos, alumno, estados, carreras_filtradas):
        self.story.append(Paragraph(titulo + ":", self.estilos["Alinear_Izquierda_Bold"]))
        self.story.append(Spacer(1, 12))

        query = AlumnosCarreras.query.filter_by(alumno_id=alumno.id)
        if carreras_filtradas:
            query = query.filter(AlumnosCarreras.carrera_id.in_(carreras_filtradas))
        carreras_alumno = query.all()

        for carrera_alumno in carreras_alumno:
            carrera = Carrera.query.get(carrera_alumno.carrera_id)
            self.story.append(Paragraph(carrera.get_descripcion_carrera() + ":", self.estilos["Alinear_Izquierda_Bold"]))
            self.story.append(Spacer(1, 12))
            self.insertar_tabla_materias(estados, carrera_alumno.carrera_id, alumno, texto_sin_datos)
            self.story.append(Spacer(1, 12))

    def insertar_tabla_materias(self, estados, id_carrera, alumno, texto_sin_datos):
        filtro = {}
        filtro["id_alumno"] = alumno.id
        filtro["id_carrera"] = id_carrera
        filtro["estados"] = estados

        materias_alumno_result = []
        for materia_alumno in filtrar_materias_alumno(filtro):
            materias_alumno_result.append(generarJSON_materia_alumno(materia_alumno))

        materias_alumno_result = sorted(materias_alumno_result, key=functools.cmp_to_key(cmp_materias_result))

        if not materias_alumno_result:
            self.story.append(Paragraph(texto_sin_datos, self.estilos["Centrado"]))
            self.story.append(Spacer(1, 12))
            return

        encabezado = []
        encabezado.append('Codigo')
        encabezado.append('Materia')

        if FINAL_PENDIENTE in estados:
            encabezado.append('Aprobación de cursada')

        if APROBADA in estados or DESAPROBADA in estados:
            encabezado.append('Estado')
            encabezado.append('Nota')
            encabezado.append('Fecha')
            encabezado.append('Forma')
            encabezado.append('Acta/Resolución')

        tbl_data = [encabezado]
        for materia in materias_alumno_result:
            fila = []
            fila.append(materia["codigo"])
            fila.append(Paragraph(self.dividir_texto_en_lineas_de_longitud_maxima(materia["nombre"],35), self.estilos["Alinear_Izquierda_Small"]))

            if FINAL_PENDIENTE in estados:
                fila.append(materia["aprobacion_cursada"])

            if APROBADA in estados or DESAPROBADA in estados:
                fila.append(materia["estado"])
                fila.append(materia["calificacion"])
                fila.append(materia["fecha_aprobacion"])
                fila.append(materia["forma_aprobacion_materia"])
                fila.append(materia["acta_o_resolucion"])
            tbl_data.append(fila)

        tbl = Table(tbl_data, hAlign='LEFT')
        tbl.setStyle(TableStyle([
            ('ALIGN',(0,0),(-1,-1),'LEFT'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ]))
        self.story.append(tbl)

    def guardar_pdf(self):
        self.doc.build(self.story)
