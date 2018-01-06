
SERVICE_BUSCAR_CARRERAS = '/api/BuscarCarreras'
SERVICE_BUSCAR_MATERIAS = '/api/BuscarMaterias'
SERVICE_OBTENER_DOCENTES = '/api/ObtenerDocentes'
SERVICE_MODIFICAR_DOCENTE = '/api/admin/ModificarDocente'


SUCCESS = 200

function do_request(url, on_success, on_error){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
           on_success(JSON.parse(xhttp.responseText));
        } else {
            //console.log(xhttp.responseText);
        }
    };
    xhttp.open("GET", url, true);
    xhttp.send();

}




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

