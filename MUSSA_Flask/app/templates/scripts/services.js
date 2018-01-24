
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
    parametro["apellido"] = apellido;
    parametro["nombre"] = nombre;
    parametro["l_ids_curso"] = JSON.stringify(l_ids_curso);

    do_request('POST', url_servicio, token, parametros, onSucces, onError);
}

function obtener_todos_los_docentes_service(token, onSuccess, onError) {
    var url_servicio = BASE_URL + '/docente/all';
    do_request('GET', url_servicio, token, {}, function(status, response) {
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
