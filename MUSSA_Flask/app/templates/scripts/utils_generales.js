function show_loading_mask() {
    $('#loader').show();
}

function hide_loading_mask() {
    $('#loader').hide();
}

function scroll_arriba() {
    $('html, body').animate({scrollTop:0}, 'slow');
}

function redirigir_a(url) {
    window.location.replace(url);
}

function getCleanedString(cadena){
   var specialChars = "!@#$^&%*()+=-[]\/{}|:<>?,.;";

   for (var i = 0; i < specialChars.length; i++) {
       cadena= cadena.replace(new RegExp("\\" + specialChars[i], 'gi'), '');
   }

   cadena = cadena.toUpperCase();

   cadena = cadena.replace(/Á/gi,"A");
   cadena = cadena.replace(/É/gi,"E");
   cadena = cadena.replace(/Í/gi,"I");
   cadena = cadena.replace(/Ó/gi,"O");
   cadena = cadena.replace(/Ú/gi,"U");
   return cadena;
}

//////////////////////////////////////////////////////////////////////

function fill_dropdown(dropdown_id, process_response, responseText){
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
}

function seleccionar_primer_opcion_no_oculta(idselector) {
    var selector = document.getElementById(idselector);
    for (var i=0; i<selector.options.length; i++) {
        if (!selector.options[i].hidden) {
            selector.selectedIndex = i;
            return;
        }
    }
    selector.selectedIndex = 0;
}