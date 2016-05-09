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