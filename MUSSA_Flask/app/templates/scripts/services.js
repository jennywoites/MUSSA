
SUCCESS = 200
SUCCESS_NO_DATA = 204

function do_request(method, page, CSRF_token, parametros, onSucces, onError) {
    var method = method || "GET";

    xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (this.status == 0 || this.readyState != 4)
            return;

        if ( this.status != SUCCESS && this.status != SUCCESS_NO_DATA) {
            onError(this.status, this.responseText);
        }
        else {
            var json_result = {};

            if (this.status == SUCCESS)
                json_result = (this.responseText == "") ? {} : JSON.parse(this.responseText)

            onSucces(this.status, json_result);
        }
    }

    var encoded_params = jQuery.param(parametros)
    var url = (method == 'GET') ? (page + '?' + encoded_params) : page;

    var async = true;
    xmlhttp.open(method, url, async);

    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.withCredentials = true;

    if (method == 'GET') {
        xmlhttp.send();
    } else {
        xmlhttp.setRequestHeader("X-CSRFToken", CSRF_token);
        xmlhttp.send(encoded_params);
    }
}

function do_request_y_abrir_PDF(method, page, CSRF_token, parametros, nombrePDF, onFinished) {
    xmlhttp = new XMLHttpRequest();
    xmlhttp.responseType = 'blob';

    xmlhttp.onreadystatechange = function() {
        if (this.status == 0 || this.readyState != 4)
            return;

        if ( this.status == SUCCESS || this.status == SUCCESS_NO_DATA) {
            var blob = new Blob([this.response], {type: 'application/pdf'});
            var link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = (nombrePDF + ".pdf");
            link.click();
        }

        if (onFinished)
            onFinished();
    }

    var async = true;
    xmlhttp.open(method, page, async);

    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.withCredentials = true;

    xmlhttp.setRequestHeader("X-CSRFToken", CSRF_token);
    xmlhttp.send(jQuery.param(parametros));
}

//////////////////////////////////////////////////////////////////////

HTTP = "http://"
IP = "localhost:"
PUERTO = "5000"
BASE_API = "/api"
BASE_URL = HTTP + IP + PUERTO + BASE_API

//*********************************************************//
//                  Servicios Docentes                     //
//*********************************************************//

function get_docente_service(token, idDocente, onSucces, onError) {
    var url_servicio = BASE_URL + '/docente/' + idDocente;
    do_request('GET', url_servicio, token, {}, onSucces, onError);
}

function eliminar_docente_service(token, idDocente, onSucces, onError) {
    var url_servicio = BASE_URL + '/docente/' + idDocente;
    do_request('DELETE', url_servicio, token, {}, onSucces, onError);
}

function modificar_docente_service(token, idDocente, apellido, nombre, l_ids_curso, onSucces, onError) {
    var url_servicio = BASE_URL + '/docente/' + idDocente;

    parametros = {};
    parametros["apellido"] = apellido;
    parametros["nombre"] = nombre;
    parametros["l_ids_cursos"] = JSON.stringify(l_ids_curso);

    do_request('POST', url_servicio, token, parametros, onSucces, onError);
}

function agrupar_docentes_service(token, ids_docentes, onSucces, onError) {
    var url_servicio = BASE_URL + '/docente/agrupar';

    parametros = {};
    parametros["ids_docentes"] = JSON.stringify(ids_docentes);

    do_request('POST', url_servicio, token, parametros, onSucces, onError);
}

function obtener_todos_los_docentes_service(token, nombre, onSuccess, onError) {
    var url_servicio = BASE_URL + '/docente/all';

    var parametros = {};
    if (nombre)
        parametros["nombre_o_apellido"] = nombre;

    do_request('GET', url_servicio, token, parametros, function(status, response) {
        onSuccess(status, response["docentes"]);
    }, onError);
}

//*********************************************************//
//                  Servicios Tematicas                    //
//*********************************************************//

function get_tematica_service(token, idTematica, onSuccess, onError) {
    var url_servicio = BASE_URL + '/tematica/' + idTematica;
    do_request('GET', url_servicio, {}, onSuccess, onError);
}

function obtener_todas_las_tematicas_service(token, solo_verificadas, onSuccess, onError) {
    var url_servicio = BASE_URL + '/tematica/all';

    parametros = {}
    parametros["solo_verificadas"] = solo_verificadas

    do_request('GET', url_servicio, parametros, onSuccess, onError);
}

//*********************************************************//
//                  Servicios Carreras                     //
//*********************************************************//

function get_todas_las_carreras_service(token, onSuccess, onError) {
    var url_servicio = BASE_URL + '/carrera/all';
    do_request('GET', url_servicio, token, {}, function(status, response) {
        onSuccess(status, response["carreras"]);
    }, onError);
}

//*********************************************************//
//                  Servicios Materias                     //
//*********************************************************//

function get_materia_service(token, idMateria, onSucces, onError) {
    var url_servicio = BASE_URL + '/materia/' + idMateria;
    do_request('GET', url_servicio, token, {}, onSucces, onError);
}

function get_materias_con_filtro_service(token, codigo, nombre, ids_carreras, onSuccess, onError) {
    var url_servicio = BASE_URL + '/materia/all';

    parametros = {};
    if (codigo)
        parametros["codigo"] = codigo;

    if (nombre)
        parametros["nombre"] = nombre;

    if (!$.isEmptyObject(ids_carreras))
        parametros["ids_carreras"] = JSON.stringify(ids_carreras);

    do_request('GET', url_servicio, token, parametros, function(status, response) {
        onSuccess(status, response["materias"]);
    }, onError);
}

//*********************************************************//
//                  Servicios Cursos                       //
//*********************************************************//

function get_cursos_con_filtro_service(token, nombre_curso, codigo_materia, id_carrera, filtrar_cursos, onSuccess, onError) {
    var url_servicio = BASE_URL + '/curso/all';

    parametros = {};

    if (nombre_curso)
        parametros["nombre_curso"] = nombre_curso;

    if (codigo_materia)
        parametros["codigo_materia"] = codigo_materia;

    if (id_carrera)
        parametros["id_carrera"] = id_carrera;

    if (filtrar_cursos)
        parametros["filtrar_cursos"] = filtrar_cursos;

    do_request('GET', url_servicio, token, parametros, function(status, response) {
        onSuccess(status, response["cursos"]);
    }, onError);
}

function modificar_curso_service(token, idCurso, ids_carreras, primer_cuatrimestre, segundo_cuatrimestre, ids_docentes,
 horarios, onSuccess, onError) {
    var url_servicio = BASE_URL + '/curso/' + idCurso;

    parametros = {};
    parametros["ids_carreras"] = JSON.stringify(ids_carreras);
    parametros["primer_cuatrimestre"] = primer_cuatrimestre;
    parametros["segundo_cuatrimestre"] = segundo_cuatrimestre;
    parametros["ids_docentes"] = JSON.stringify(ids_docentes);
    parametros["horarios"] = JSON.stringify(horarios);

    do_request('POST', url_servicio, token, parametros, onSuccess, onError);
}

//*********************************************************//
//                  Servicios Alumno                       //
//*********************************************************//

function modificar_alumno_service(token, padron, onSuccess, onError) {
    var url_servicio = BASE_URL + '/alumno';

    parametros = {}
    parametros["padron"] = padron;

    do_request('POST', url_servicio, token, parametros, onSuccess, onError);
}

function obtener_materias_pendientes_service(token, id_carrera, onSuccess, onError) {
    var url_servicio = BASE_URL + '/alumno/materia/pendientes';

    parametros = {}
    parametros["id_carrera"] = id_carrera;

    do_request('GET', url_servicio, token, parametros, function(status, response) {
        onSuccess(status, response["materias_alumno"]);
    }, onError);
}

function finalizar_encuesta_alumno_service(token, idEncuestaAlumno, onSuccess, onError) {
    var url_servicio = BASE_URL + '/alumno/encuesta/' + idEncuestaAlumno;

    parametros = {}
    parametros["finalizada"] = true;

    do_request('POST', url_servicio, token, parametros, onSuccess, onError);
}

function guardar_respuestas_encuesta_alumno_service(token, idEncuestaAlumno, categoria, respuestas, onSuccess, onError) {
    var url_servicio = BASE_URL + '/alumno/encuesta/' + idEncuestaAlumno + '/respuestas';

    parametros = {}
    parametros["categoria"] = categoria;
    parametros["respuestas"] = JSON.stringify(respuestas);

    do_request('POST', url_servicio, token, parametros, onSuccess, onError);
}

function descargar_nota_al_decano_service(token, objeto, motivo, telefono, domicilio, localidad, dni, anio_ingreso, nota_extendida, onFinished) {
    var url_servicio = BASE_URL + '/alumno/formulario/nota_al_decano';

    parametros = {}
    parametros["objeto"] = objeto;
    parametros["motivo"] = motivo;
    parametros["telefono"] = telefono;
    parametros["domicilio"] = domicilio;
    parametros["localidad"] = localidad;
    parametros["dni"] = dni;
    parametros["anio_ingreso"] = anio_ingreso;
    parametros["nota_extendida"] = nota_extendida;

    do_request_y_abrir_PDF('PUT', url_servicio, token, parametros, 'NotaAlDecano', onFinished);
}

function descargar_lista_de_materias_service(token, carreras, tipos_de_materias, onFinished) {
    var url_servicio = BASE_URL + '/alumno/formulario/materias_alumno';

    parametros = {}
    parametros["carreras"] = JSON.stringify(carreras);
    parametros["tipos_de_materias"] = JSON.stringify(tipos_de_materias);

    do_request_y_abrir_PDF('PUT', url_servicio, token, parametros, 'Materias', onFinished);
}

function generar_plan_de_estudios_greedy_service(token, carrera, max_cant_cuatrimestres, max_cant_materias, max_horas_cursada,
    max_horas_extras, puntaje_minimo_cursos, cuatrimestre_inicio, anio_inicio, horarios_invalidos, tematicas,
    aprobacion_finales, cursos_preseleccioandos, trabajo_final, orientacion, onSuccess, onError) {

    var algoritmo = 0;
    generar_plan_de_estudios_service(token, carrera, max_cant_cuatrimestres, max_cant_materias, max_horas_cursada,
            max_horas_extras, puntaje_minimo_cursos, cuatrimestre_inicio, anio_inicio, horarios_invalidos, tematicas,
            aprobacion_finales, cursos_preseleccioandos, trabajo_final, orientacion, algoritmo, onSuccess, onError);
}

function generar_plan_de_estudios_PLE_service(token, carrera, max_cant_cuatrimestres, max_cant_materias, max_horas_cursada,
    max_horas_extras, puntaje_minimo_cursos, cuatrimestre_inicio, anio_inicio, horarios_invalidos, tematicas,
    aprobacion_finales, cursos_preseleccioandos, trabajo_final, orientacion, onSuccess, onError) {

    var algoritmo = 1;
    generar_plan_de_estudios_service(token, carrera, max_cant_cuatrimestres, max_cant_materias, max_horas_cursada,
        max_horas_extras, puntaje_minimo_cursos, cuatrimestre_inicio, anio_inicio, horarios_invalidos, tematicas,
        aprobacion_finales, cursos_preseleccioandos, trabajo_final, orientacion, algoritmo, onSuccess, onError);
}

function generar_plan_de_estudios_service(token, carrera, max_cant_cuatrimestres, max_cant_materias, max_horas_cursada,
    max_horas_extras, puntaje_minimo_cursos, cuatrimestre_inicio, anio_inicio, horarios_invalidos, tematicas,
    aprobacion_finales, cursos_preseleccionados, trabajo_final, orientacion, algoritmo, onSuccess, onError) {
    var url_servicio = BASE_URL + '/alumno/planDeEstudios';

    parametros = {}
    parametros["carrera"] = carrera;
    parametros["max_cant_cuatrimestres"] = max_cant_cuatrimestres;
    parametros["max_cant_materias"] = max_cant_materias;
    parametros["max_horas_cursada"] = max_horas_cursada;
    parametros["max_horas_extras"] = max_horas_extras;
    parametros["puntaje_minimo_cursos"] = puntaje_minimo_cursos;
    parametros["cuatrimestre_inicio"] = cuatrimestre_inicio;
    parametros["anio_inicio"] = anio_inicio;
    parametros["horarios_invalidos"] = JSON.stringify(horarios_invalidos);

    parametros["tematicas"] = JSON.stringify(tematicas);
    parametros["aprobacion_finales"] = JSON.stringify(aprobacion_finales);
    parametros["cursos_preseleccionados"] = JSON.stringify(cursos_preseleccionados);
    parametros["trabajo_final"] = trabajo_final;
    parametros["orientacion"] = orientacion;
    parametros["algoritmo"] = algoritmo;

    do_request('PUT', url_servicio, token, parametros, onSuccess, onError);
}
