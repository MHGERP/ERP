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

$("#btn-add").click(function() {
    $("#info_modal").removeAttr("iid");
});
$("#btn_save_principal").click(function() {
    var id_work_order = $("#id_work_order").val();   
    Dajaxice.techdata.addOrUpdateSinglePrincipalItem(function(data) {
        if(data == "ok") {
            alert("保存成功");
            refresh();
        }
        else alert("保存失败");
    }, {
        "id_work_order": id_work_order,
        "form": $("#principal_form").serialize(),
        "iid": $("#info_modal").attr("iid"),
    })
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

$(document).on("dblclick", ".tr_materiel", function() {
    var inventory_type = $(".form-search").attr("itype");
    var iid = $(this).attr("iid");
    $("#info_modal").attr("iid", iid);
    Dajaxice.techdata.getItemInfo(function(data) {
        $("#principal_form").html(data);
    }, {
       "iid": iid,
       "inventory_type": inventory_type,
    });
    $("#info_modal").modal("show");
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

$("#id_goto_next").click(function() {
    var cur_iid = $("#info_modal").attr("iid");
    var row = $("tr[iid='" + cur_iid + "']");
    var row_next = row.next(".tr_materiel");
    var next_iid = row_next.attr("iid");
    if(!row_next.html()) alert("本条为最后一条！");
    else {
    var inventory_type = $(".form-search").attr("itype");
    Dajaxice.techdata.getItemInfo(function(data) {
        $("#principal_form").html(data);}, {
       "iid": row_next.attr("iid"),
       "inventory_type": inventory_type,});
        $("#info_modal").modal("show");
      $("#info_modal").attr("iid",next_iid);

}
});

$("#id_goto_prev").click(function() {
    var cur_iid = $("#info_modal").attr("iid");
    var row = $("tr[iid='" + cur_iid + "']");
    var row_prev = row.prev(".tr_materiel");
    var prev_iid = row_prev.attr("iid");
    if(!row_prev.html()) alert("本条为第一条！");
    else {
    var inventory_type = $(".form-search").attr("itype");
    Dajaxice.techdata.getItemInfo(function(data) {
        $("#principal_form").html(data);}, {
       "iid": row_prev.attr("iid"),
       "inventory_type": inventory_type,});
        $("#info_modal").modal("show");
        $("#info_modal").attr("iid",prev_iid);

}
});

