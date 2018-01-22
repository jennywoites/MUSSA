function show_loading_mask() {
    $('#loader').show();
}

function hide_loading_mask() {
    $('#loader').hide();
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
