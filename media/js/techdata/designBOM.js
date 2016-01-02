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
    $("#designBOM_edit_modal").attr("iid", iid);
    Dajaxice.techdata.getDesignBOMForm(getDesignBOMFormCallback, {"iid" : iid});
});

function getDesignBOMFormCallback(data) {
    $("#materiel_div").html(data.materiel_form);
    $("#circulationroute_div").html(data.circulationroute_form);
    $("#designBOM_edit_modal").modal();
}

$(document).on("click","#save_desginBOM_btn", function(){
    var iid = $("#designBOM_edit_modal").attr("iid");
    //alert(iid);
    Dajaxice.techdata.saveDesignBOM(saveDesignBOMCallback, 
                                    {
                                        'iid' : iid,
                                        'materiel_form' :$("#materiel_form").serialize(),
                                        'circulationroute_form' : $("#circulationroute_form").serialize()
                                    });
});

function saveDesignBOMCallback(data) {
    if(data.status == "ok") {
        alert("修改成功！");
    }
    else {
        if(data.circulationroute_error == "1")
            alert("流转路线必须连续");
        if(data.materiel_error == "1")
            alert("#materiel_div").html(data.html);
    }
}
