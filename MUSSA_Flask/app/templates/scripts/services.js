
SERVICE_BUSCAR_CARRERAS = '/api/BuscarCarreras'
SERVICE_BUSCAR_MATERIAS = '/api/BuscarMaterias'

SUCCESS = 200

function do_request(page, onSucces, onError){
    xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if ( this.status != SUCCESS ){
            onError(this.status, this.responseText);
        }
        else{
            json_result = (this.responseText == "") ? {} : JSON.parse(this.responseText)
            onSucces(this.status, json_result);
        }
    }

    xmlhttp.open("GET", page, true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send();
}
