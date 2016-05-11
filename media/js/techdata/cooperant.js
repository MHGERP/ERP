$(document).ready(refresh);
$("#order_search").click(refresh);
function refresh(){
    var id_work_order = $("#id_work_order").val();
    var inventory_type = $(".form-search").attr("itype");
    Dajaxice.techdata.getInventoryTables(refreshCallBack, {"id_work_order": id_work_order, "inventory_type": inventory_type});
}
function refreshCallBack(data) {
    $(".widget-box").html(data);
}
$(document).on("click", "#fast_generate", function(){
    var id_work_order = $("#id_work_order").val();
    var inventory_type = $(".form-search").attr("itype");
    Dajaxice.techdata.autoSetInventoryLabel(function(data) {
        alert("生成成功！");
        refresh();
    }, {
        "id_work_order": id_work_order,
        "inventory_type": inventory_type,
    })
});

$("#btn-add").click(function() {
    var index = $("#input-index").val()
    var id_work_order = $("#id_work_order").val();
    var inventory_type = $(".form-search").attr("itype");
    Dajaxice.techdata.addSingleItem(function(data) {
        if(data.success) refresh();
        alert(data.remark);
    }, {
        "id_work_order": id_work_order,
        "index": index,
        "inventory_type": inventory_type,
    })
});

$(document).on("dblclick", ".tr_materiel", function() {
    var iid = $(this).attr("iid");
    $("#info_modal").attr("iid", iid);
    $("#info_modal").modal("show");
});
$("#btn_save").click(function() {
    var remark = $("#input-remark").val();
    var iid = $("#info_modal").attr("iid");
    var inventory_type = $(".form-search").attr("itype");
    Dajaxice.techdata.updateDetailItemInfo(refresh, {
        "remark": remark,
        "iid": iid,
        "inventory_type": inventory_type,
    });
});
$(document).on("click", ".btn-remove", function(){
    if (confirm("是否确定删除？")) {
        var inventory_type = $(".form-search").attr("itype");
        var iid = $(this).parent().parent().attr("iid");
        Dajaxice.techdata.deleteSingleItem(function() {
            alert("删除成功！");
            refresh();
        }, {"iid": iid,  "inventory_type": inventory_type});
    }
});

$(document).on("click", ".btn-mark", function() {
    mark_span = $(this).parent();
    var inventory_type = $(".form-search").attr("itype");
    var id_work_order = $("#id_work_order").val();
    var step = $(this).attr("args");
    Dajaxice.techdata.detailMark(markCallBack, {"id_work_order": id_work_order, 
                                     "step": step, 
                                     "inventory_type": inventory_type,
    });
});
function markCallBack(data) {
    if(data.ret) {
        mark_span.html(data.mark_user);
    }
    else {
        alert(data.warning);
    }
}


