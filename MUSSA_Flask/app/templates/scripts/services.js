
SUCCESS = 200
SUCCESS_NO_DATA = 204

function do_request(method, page, parametros, onSucces, onError) {
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
        xmlhttp.setRequestHeader("X-CSRFToken", "{{ csrf_token() }}");
        xmlhttp.send(encoded_params);
    }
}

//////////////////////////////////////////////////////////////////////

SERVICE_BUSCAR_CARRERAS = '/api/BuscarCarreras'
SERVICE_BUSCAR_MATERIAS = '/api/BuscarMaterias'
SERVICE_MODIFICAR_DOCENTE = '/api/admin/ModificarDocente'

HTTP = "http://"
IP = "localhost:"
PUERTO = "5000"
BASE_API = "/api"
BASE_URL = HTTP + IP + PUERTO + BASE_API

//*********************************************************//
//                  Servicios Docentes                     //
//*********************************************************//

function get_docente_service(idDocente, onSucces, onError) {
    var url_servicio = BASE_URL + '/docente/' + idDocente;
    do_request('GET', url_servicio, {}, onSucces, onError);
}

function eliminar_docente_service(idDocente, onSucces, onError) {
    debugger;
    var url_servicio = BASE_URL + '/docente/' + idDocente;
    do_request('DELETE', url_servicio, {}, onSucces, onError);
}

function obtener_todos_los_docentes_service(onSucces, onError) {
    var url_servicio = BASE_URL + '/docente/all';
    do_request('GET', url_servicio, {}, function(status, response) {
        onSucces(status, response["docentes"]);
    }, onError);
}

//*********************************************************//
//                  Servicios Materias                     //
//*********************************************************//

function get_tematica_service(idTematica, onSucces, onError) {
    var url_servicio = BASE_URL + '/materia/tematica/' + idTematica;
    do_request('GET', url_servicio, {}, onSucces, onError);
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
