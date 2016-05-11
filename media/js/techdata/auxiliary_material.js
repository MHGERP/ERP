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
    Dajaxice.techdata.getMaterielDetailInfo(getInfoCallBack, {"iid": iid});
    Dajaxice.techdata.getAuxiliary(getAuxiliaryCallBack, {"iid": iid});
}
function getInfoCallBack(data) {
    $("#base-info-area").html("<h5>原始数据</h5>"+data);
}
function getAuxiliaryCallBack(data) {
    $("#auxiliary-form-area").html("<h5>辅材定额录入</h5>"+data);
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
$(document).on("click", "#id_save", function() {
    var iid = $("#card_modal").attr("iid");
    Dajaxice.techdata.updateAuxiliary(updateAuxiliaryCallBack, {    "iid":iid,
                                                                    "form": $("#auxiliary_form").serialize()});
});
function updateAuxiliaryCallBack(data){
    if(data=="ok"){
        alert("保存成功");
    }
    else{
        alert("保存失败");
    }
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