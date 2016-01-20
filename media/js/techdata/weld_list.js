$(document).ready(refresh);
$("#order_search").click(refresh);

function refresh() {
    var id_work_order = $("#id_work_order").val();
    Dajaxice.techdata.getWeldSeamList(refreshCallBack, {"id_work_order": id_work_order, });
}
function refreshCallBack(data) {
    if(data.read_only) {
        $("#id_save").hide();
        $("#id_calculate").hide();
    }
    else {
        $("#id_save").show();
        $("#id_calculate").show();
    }
    $("#widget-box").html(data.html);
}
function refreshSingleRow() {
    var iid = $("#card_modal").attr("iid");
    Dajaxice.techdata.getSingleWeldSeamInfo(refreshSingleCallBack, {"iid": iid})
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
    Dajaxice.techdata.getWeldSeamCard(getCardCallBack, {"full": true, "iid": iid});
}
function getCardCallBack(data) {
    $("#weld_seam_card").html(data);
}

$("#id_save").click(function() {
    var iid = $("#card_modal").attr("iid");
    Dajaxice.techdata.modifyWeldSeam(saveCallBack, {"iid": iid, "form": $("#weld_seam_card").serialize()})
});
function saveCallBack(data) {
    if(data == "ok") {
        refreshSingleRow();
        alert("焊缝信息修改成功！");
    }
    else {
        $("#weld_seam_card").html(data);
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

$(document).on("click", "#btn_write_confirm", function() {
    var id_work_order = $("#id_work_order").val();   
    Dajaxice.techdata.weldListWriterConfirm(writerConfirmCallBack, {"id_work_order": id_work_order})
});
function writerConfirmCallBack(data) {
    if(data.ret) {
        $("#btn_write_confirm").removeClass("btn-primary").addClass("btn-warning").html("编制完成");
        $("#span_write").html("编制人：" + data.user);
    }
}

$(document).on("click", "#btn_review_confirm", function() {
    var id_work_order = $("#id_work_order").val();   
    Dajaxice.techdata.weldListReviewerConfirm(reviewerConfirmCallBack, {"id_work_order": id_work_order})
});
function reviewerConfirmCallBack(data) {
    if(data.ret) {
        $("#btn_review_confirm").removeClass("btn-primary").addClass("btn-warning").html("审核完成");
        $("#span_review").html("审核人：" + data.user);
    }
    else {
        alert("未完成编制，无法审核！");
    }
}
