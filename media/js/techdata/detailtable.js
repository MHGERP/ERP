$(document).on("click", "#order_search", function(){
    //var s = $('select option:selected').val();
    var s = $("#table_select").val();
    var order = $('#id_work_order').val();
    if (s == "0")
        $("#detail_table").html("");
    else if (s == "1")
        Dajaxice.techdata.firstFeeding(tableCallback, {"order" : order});
    else if (s == "2")
        Dajaxice.techdata.principalMaterial(tableCallback, {"order" : order});
    else if (s == "3")
        Dajaxice.techdata.auxiliaryMaterial(tableCallback, {"order" : order});
    else if (s == "4")
        Dajaxice.techdata.weldList(tableCallback, {"order" : order});
    else if (s == "5")
        Dajaxice.techdata.weldQuota(tableCallback, {"order": order});
    else if (s == "6")
        Dajaxice.techdata.techBoxWeld(tableCallback, {"order" : order});
    else if (s == "7")
        Dajaxice.techdata.boxOutBought(tableCallback, {"order" : order});
});

function tableCallback(data) {
   $("#detail_table").html(data);
}



$(document).on("click", ".tr_materiel", function() {
    var iid = $(this).attr("iid");
    fill(iid);
});

function fill(iid) {
    $("#card_modal").attr("iid", iid);
    Dajaxice.techdata.getAuxiliaryMaterielInfo(getInfoCallBack, {"iid": iid});
}

function getInfoCallBack(data) {
    $("#base-info-area").html(data.auxiliary_materiel_info_html);
    $("#type_in").html(data.detail_table_html);
}

$(document).on("click","#id_success",function(){
    $("#id_quota").val($("#id_total_weight").val()*$("#id_factor").val());
});

// $(document).on("click","#id_confirm",function(){
    
//     Dajaxice.techdata.saveAuxiliaryMaterielInfo(saveAuxiliaryMaterielInfoCallBack, {"iid": iid});
// });
// function saveAuxiliaryMaterielInfoCallBack(){

// }
$("#id_goto_next").click(function(){
   var cur_iid = $("#card_modal").attr("iid");
   var row = $("tr[iid='" + cur_iid + "']");
   var row_next = row.next(".tr_materiel");
   if(!row_next.html()) alert("本条为最后一条");
   else fill(row_next.attr("iid"));
});

$("#id_goto_prev").click(function(){
   var cur_iid = $("#card_modal").attr("iid");
   var row = $("tr[iid='" + cur_iid + "']");
   var row_prev = row.prev(".tr_materiel");
   if(!row_prev.html()) alert("本条为第一条");
   else fill(row_prev.attr("iid"));
});
