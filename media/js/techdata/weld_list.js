$(document).ready(refresh);
$("#order_search").click(refresh);

function refresh() {
    var id_work_order = $("#id_work_order").val();
    Dajaxice.techdata.getWeldSeamList(refreshCallBack, {"id_work_order": id_work_order, });
}
function refreshCallBack(data) {
    $("#widget-box").html(data);
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
