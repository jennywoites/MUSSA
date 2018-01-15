
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

SERVICE_BUSCAR_CARRERAS = '/api/BuscarCarreras'
SERVICE_BUSCAR_MATERIAS = '/api/BuscarMaterias'

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

function obtener_todos_los_docentes_service(token, onSucces, onError) {
    var url_servicio = BASE_URL + '/docente/all';
    do_request('GET', url_servicio, token, {}, function(status, response) {
        onSucces(status, response["docentes"]);
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

//////////////////////////////////////////////////////////////////////

function fill_dropdown(dropdown_id, service_url, process_response){
    do_request(service_url, function(responseText){
        process_data = process_response(responseText);
        content = "";
        for(var i=0; i<process_data.length; i++) {
            current_data = process_data[i];
            content += '<option';
            if ("id" in current_data)
                content += ' id="' + current_data["id"] + '"';
            if ("value" in current_data)
                content += ' value="' + current_data["value"] + '"';
            content += ">";
            if ("text" in current_data)
                content += current_data["text"];
            content += "</option>";
        }
        $("#" + dropdown_id).html(content);

    });
}
