$(document).ready(refresh);
$("#order_search").click(refresh);
function refresh(){
    var id_work_order = $("#id_work_order").val();
    Dajaxice.techdata.getProcessBOM(refreshCallBack, {"id_work_order": id_work_order, });
}
function refreshCallBack(data) {
    $("#widget-box").html(data);
}

function refreshSingleRow() {
    var iid = $("#card_modal").attr("iid");
    Dajaxice.techdata.getSingleProcessBOM(refreshSingleCallBack, {"iid": iid})
}
function refreshSingleCallBack(data) {
    var cur_iid = $("#card_modal").attr("iid");
    $(".row_1[iid='" + cur_iid + "']").html(data.html);
    $(".row_2[iid='" + cur_iid + "']").html(data.html2);
    row.html(data.html);
}
$(document).on("dblclick", ".tr_materiel", function() {
    var iid = $(this).attr("iid");
    fill(iid);
    $('#card_modal').modal('show')
});

function fill(iid) {
    $("#card_modal").attr("iid", iid);
    Dajaxice.techdata.getMaterielInfo(getInfoCallBack, {"iid": iid});
    Dajaxice.techdata.getProcess(getProcessCallBack, {"iid": iid});
}
function getInfoCallBack(data) {
    $("#base-info-area").html(data);
}
function getProcessCallBack(data) {
    $("#processing-area").html(data);
}

$("#btn_save").click(function() {
    var iid = $("#card_modal").attr("iid");
    var materiel_form = $("#base-info_form").serialize();
    var processing_form = $("#processing_form").serialize();
    Dajaxice.techdata.saveProcess(saveCallback, {"iid": iid, 
                                  "materiel_form": materiel_form,
                                  "processing_form": processing_form});
});
function saveCallback(data) {
    if(data.status == "ok") {
        refreshSingleRow();
        alert("修改成功！");
    }
    else {
        if(data.processing_error == "1")
            alert("工序路线必须连续");
        if(data.materiel_error == "1")
            alert("#materiel_div").html(data.html);
    }
       
}

$("#weldseam_edit").click(function() {
    Dajaxice.techdata.getWeldSeamCard(getCardCallBack, {}); 
});
function getCardCallBack(data) {
    $("#weld_seam_card").html(data);
}

$(document).on("click", "#btn_cancel", function() {
    $("#weld_seam_card").html("");
});


$(document).on("click", "#btn_weldseam_confirm", function() {
    var iid = $("#card_modal").attr("iid");
    Dajaxice.techdata.addWeldSeam(addWeldSeamCallBack, {"iid": iid, "form": $("#weld_seam_card").serialize()})
});
function addWeldSeamCallBack(data) {
    if(data == "ok") {
        alert("焊缝添加成功！");
        $("#weld_seam_card").html("");
    }
    else {
        $("#weld_seam_card").html(data);
    }
}

$("#id_goto_next").click(function() {
    var cur_iid = $("#card_modal").attr("iid");
    var row = $("tr[iid='" + cur_iid + "']");
    var row_next = row.next(".row_1");
    if(!row_next.html()) alert("本条为最后一条！");
    else fill(row_next.attr("iid"));
});

$("#id_goto_prev").click(function() {
    var cur_iid = $("#card_modal").attr("iid");
    var row = $("tr[iid='" + cur_iid + "']");
    var row_prev = row.prev(".tr_materiel");
    if(!row_prev.html()) alert("本条为第一条！");
    else fill(row_prev.attr("iid"));
});

$(document).on("click", ".btn_edit_transfer_card", function() {
    var iid = $(this).parent().parent().attr("iid");
    location.href = "/techdata/transferCardEdit?iid=" + iid;
});

var mark_span;

$(document).on("click", ".btn-mark", function() {
    mark_span = $(this).parent();
    var id_work_order = $("#id_work_order").val();
    var step = $(this).attr("args");
    Dajaxice.techdata.processBOMMark(markCallBack, {"id_work_order": id_work_order, "step": step, });
});
function markCallBack(data) {
    if(data.ret) {
        mark_span.html(data.mark_user);
    }
    else {
        alert(data.warning);
    }
}

$(document).on("click", "#quick_edit", function(){
    var rounte = $(id_rounte).attr("value");
     a = rounte.split(/[;|；]/);
     for(var i = 1;i<=12;i++){

     var options = $("#id_GX"+i).children("option");
 
     for (var j = 0; j < options.length; j++) {
         if (options[j].text == a[i-1]){
           options[j].selected = true;
           break;
           }
        
     }
 }

   
});