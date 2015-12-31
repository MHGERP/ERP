$(document).ready(refresh);
$("#order_search").click(refresh);
function refresh() {
    var id_work_order = $("#id_work_order").val();
    Dajaxice.techdata.getDesignBOM(refreshCallBack, {"id_work_order" : id_work_order, });
}
function refreshCallBack(data) {
    $("#widget-box").html(data);
}

//$("#designBOM_table tbody tr").click(function(){
//    alert("cao");
//    Dajaxice.techdata.getDesignBOMForm(getDesignBOMFormCallback, {});
//});

$(document).on("click", "#designBOM_table tbody tr", function(){
    var iid = $(this).attr("iid");
    Dajaxice.techdata.getDesignBOMForm(getDesignBOMFormCallback, {"iid" : iid});
});

function getDesignBOMFormCallback(data) {
    $("#materiel_div").html(data.materiel_form);
    $("#circulationroute_div").html(data.circulationroute_form);
    $("#designBOM_edit_modal").modal();
}

$("#save_desginBOM_btn").click(function(){
    Dajaxice.techdata.saveDesignBOM(saveDesignBOMCallback, {});
});

function savedesignBOMCallback(data) {
    
}
