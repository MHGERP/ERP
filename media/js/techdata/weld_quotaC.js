$(document).ready(refresh);
$(document).on("click", "#order_search", refresh);
function refresh() {
    var id_work_order = $("#id_work_order").val();

    Dajaxice.techdata.getWeldSeamWeight(refreshCallBack, {"id_work_order": id_work_order, });

        
}
function refreshCallBack(data) {
    $(".widget-box2").html(data);
    // $("#detail_table").html(data);
}
$(document).on("click", "#btn_weld_quota_write_confirm", function() {
    var id_work_order = $("#id_work_order").val();   
    Dajaxice.techdata.weldQuotaWriterConfirm(weldQuotaWriterConfirmCallBack, {"id_work_order": id_work_order})
});
function weldQuotaWriterConfirmCallBack(data) {
    if(data.ret) {
        $("#span_write").html("编制人：" + data.user);
    }
}

$(document).on("click", "#btn_weld_quota_review_confirm", function() {
    var id_work_order = $("#id_work_order").val();   
    Dajaxice.techdata.weldQuotaReviewerConfirm(weldQuotaReviewerConfirmCallBack, {"id_work_order": id_work_order})
});
function weldQuotaReviewerConfirmCallBack(data) {
    if(data.ret) {
        $("#span_review").html("审核人：" + data.user);
    }
    else {
        alert("未完成编制，无法审核！");
    }
}
var iid;
$(document).on("dblclick", ".tr_materiel td", function() {
    if($(this).index() != 0) {
        iid = $(this).parent().attr("iid");
        fill(iid);
        $("#card_modal").modal();
    }
});
function fill(iid) {
    $("#card_modal").attr("iid", iid);
    Dajaxice.techdata.getWeldQuotaCard(getCardCallBack, {"iid": iid});
}
function getCardCallBack(data) {
    $("#weld_quota_card").html(data);
}

$(document).on("click", "#id_add", function() {
    var work_order = $("#id_work_order").val();

    Dajaxice.techdata.getMaterial(getMaterialCallBack, {      
                                                            "work_order":work_order,})
    
});
var weld_quota_id
function getMaterialCallBack(data){
    $("#widget_box3").html(data);
    $("#card_modal_add").modal();
}
$(document).on("click", "#add_save", function() {
    var work_order = $("#id_work_order").val();
    // var weld_material = $("#id_weld_material2").val();
    // var size = $("#id_size2").val();
    // var stardard = $("#id_stardard2").val();
    // var quota = $("#id_quota2").val();
    // var remark = $("#id_remark2").val();
    Dajaxice.techdata.addWeldQuota(addWeldQuotaCallBack, {      "form": $("#widget_box3").serialize(),
                                                                "work_order":work_order,})
    
});

function addWeldQuotaCallBack(data){
     if(data == "ok") {
            alert("新增成功！");
            refresh();
        }
        else {
            alert("新增失败！");
        }
}

$(document).on("click", "#quick_generate", function() {
    var id_work_order = $("#id_work_order").val();
    Dajaxice.techdata.saveWeldQuota(saveWeldQuotaCallBack, {"id_work_order": id_work_order})
});

function saveWeldQuotaCallBack(data){
     if(data == "ok") {
            alert("生成成功！");
            refresh();
        }
        else {
            alert("生成失败！");
        }
}

$(document).on("click", "#id_save", function() {
    var categories = $("#id_categories").val();
    var weld_material = $("#id_weld_material").val();
    var size = $("#id_size").val();
    var stardard = $("#id_stardard").val();
    var quota = $("#id_quota").val();
    var remark = $("#id_remark").val();
    Dajaxice.techdata.updateWeldQuota(updateWeldQuotaCallBack, {"iid": iid,
                                                                "categories":categories,
                                                                "weld_material":weld_material,
                                                                "size":size,
                                                                "stardard":stardard,
                                                                "quota":quota,
                                                                "remark":remark,})
});

function updateWeldQuotaCallBack(data){
     if(data == "ok") {
            alert("保存成功！");
            refresh();
        }
        else {
            alert("保存失败！");
        }
}


$(document).on("click", "#id_delete", function() {
    var did = $(this).attr("did");
    Dajaxice.techdata.deleteWeldQuota(deleteWeldQuotaCallBack, {"did": did})
});

function deleteWeldQuotaCallBack(data){
     if(data == "ok") {
            alert("删除成功！");
            refresh();
        }
        else {
            alert("删除失败！");
        }
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