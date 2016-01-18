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
    var row = $("tr[iid='" + cur_iid + "']");
    row.html(data);
}
$(document).on("click", ".tr_materiel", function() {
    var iid = $(this).attr("iid");
    fill(iid);
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
    $("#process_table").html(data);
}

$("#id_add_process").click(function() {
    var process_id = $("#id_process").val();
    var iid = $("#card_modal").attr("iid");
    Dajaxice.techdata.addProcess(refreshProcess, {"process_id": process_id, "iid": iid, });
});

$(document).on("click", ".btn-del-process", function() {
    var pid = $(this).attr("pid");
    Dajaxice.techdata.deleteProcess(refreshProcess, {"pid": pid});
});

function refreshProcess() {
    var iid = $("#card_modal").attr("iid");
    refreshSingleRow();
    Dajaxice.techdata.getProcess(getProcessCallBack, {"iid": iid});
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

$(document).on("click", ".btn-save-process", function() {
    var tr = $(this).parent().parent();
    var iid = tr.attr("iid");
    var index = tr.find("input").eq(0).val();
    var hour = tr.find("input").eq(1).val();
    var instruction = tr.find("input").eq(2).val();
    Dajaxice.techdata.saveProcessInfo(saveProcessInfoCallBack, {"iid": iid,
                                                                "index": index,
                                                                "hour": hour,
                                                                "instruction": instruction});
});
function saveProcessInfoCallBack(data) {
    if(data == "ok") alert("保存成功！");
    else alert("格式有错误！");
}
$("#id_goto_next").click(function() {
    var cur_iid = $("#card_modal").attr("iid");
    var row = $("tr[iid='" + cur_iid + "']");
    var row_next = row.next(".tr_materiel");
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
    location.href = "/techdata/transfer_card_edit?iid=" + iid;
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
