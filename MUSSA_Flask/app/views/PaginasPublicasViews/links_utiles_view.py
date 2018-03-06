from app.views.base_view import main_blueprint
from flask import render_template


@main_blueprint.route('/links_utiles')
def links_utiles_page():
    links = [
        {
            "URL": 'http://fi.uba.ar/',
            "MSJ_URL": 'Facultad de Ingeniería',
            "DESCRIPCION": 'Página oficial de la Facultad de Ingeniería de la Universidad de Buenos Aires'
        },
        {
            "URL": 'https://francospada.github.io/organizador-fiuba/',
            "MSJ_URL": 'Organizador de Horarios',
            "DESCRIPCION": 'Organizador de Horarios para que puedas probar combinaciones de horarios para el cuatrimestre actual en base a los horarios publicados por la facultad.'
        },
        {
            "URL": 'http://campus.fi.uba.ar/',
            "MSJ_URL": 'Campus',
            "DESCRIPCION": 'Campus virtual FIUBA. Algunas materias utilizan el campus como vía de comunicación o para compartir archivos, subir trabajos prácticos, etc.'
        },
        {
            "URL": 'https://www.facebook.com/groups/fiubaconsultas2/',
            "MSJ_URL": 'FIUBA Consultas',
            "DESCRIPCION": 'Grupo de Facebook de alumnos de la FIUBA. En él se hacen consultas muy diversas (incluidas las de ingresantes), algunos chistes, información importante, etc.'
        },
        {
            "URL": 'http://wiki.foros-fiuba.com.ar/',
            "MSJ_URL": 'Wiki Foros-FIUBA',
            "DESCRIPCION": 'Ejercicios, trabajos prácticos y exámenes de las distintas materias subidos por alumnos.'
        },
        {
            "URL": 'http://www.foros-fiuba.com.ar/',
            "MSJ_URL": 'Foros FIUBA',
            "DESCRIPCION": 'Foro de alumnos de FIUBA. Mucha información ya ha quedado desactualizada pero es posible encontrar información sobre algunas materias y preguntas de diversa índole.'
        },
        {
            "URL": 'http://www.fi.uba.ar/es/node/764',
            "MSJ_URL": 'Solicitud de Título',
            "DESCRIPCION": 'Requisitos y trámites necesarios para tramitar el título FIUBA.',
            "COMENTARIO_OCULTO": 'Si llegaste a este punto congrats! =D'
        },
        {
            "URL": 'http://sietgraduados.rec.uba.ar/',
            "MSJ_URL": 'Seguimiento del Título',
            "DESCRIPCION": 'Requisitos y trámites necesarios para tramitar el título FIUBA.',
            "COMENTARIO_OCULTO": 'Sentate a esperar porque este trámite dura entre un año y medio y dos años :('
        },
    ]

    return render_template('pages/links_utiles_page.html',
                           links=links)
