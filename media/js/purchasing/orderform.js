var pendingArray = Array();

$(document).ready(refresh);

function refresh() {
    var index = $("#index").val();
    var can_choose = (1 == $("#status").attr("args"));
    Dajaxice.purchasing.getOrderFormItems(getItemsCallBack, {
        "index": index,
        "can_choose": can_choose,
    });

    Dajaxice.purchasing.getOngoingBidList(getBidListCallBack, {});
}
function getBidListCallBack(data) {
    $(".bid-select").each(function() { 
        $(this).html(data);   
    });
}
function getItemsCallBack(data) {
    $("#item_table").html(data);
}

$("#btn-save").click(function() {
    var id = $("#bid_modal").attr("args");
    if(confirm("是否确认保存？")) {
        Dajaxice.purchasing.newBidSave(saveCallBack, {"id": id, "pendingArray": pendingArray, });
        return true;
    }
    return false;
});
function saveCallBack() {
    refresh();
}
$("#btn-finish").click(function() {
    var id = $("#bid_modal").attr("args");
    if(confirm("是否确认完成编制？")) {
        Dajaxice.purchasing.newBidFinish(finishCallBack, {"id": id});
        return true;
    }
    return false;
});
function finishCallBack() {
    refresh();
}

$(".btn-open").click(function() {
    if($(this).hasClass("clear")) {
        pendingArray = Array();
    }
    var id = $($(this).attr("data-source")).val(); // datatable index not bid_id
    Dajaxice.purchasing.getBidForm(getBidCallBack, {"bid_id": id, "pendingArray": pendingArray, })
});

$("#new_purchase_btn").click(function() {
    Dajaxice.purchasing.newBidCreate(getBidCallBack, {});
});

function getBidCallBack(data) {
    $("input#bid_id").val(data.bid_id);
    $("div.table-div").html(data.html);
    $("#bid_modal").attr("args", data.id);
    Dajaxice.purchasing.getOngoingBidList(getBidListCallBack, {});
}
$(document).on("click", "input#select_all", function(){
    var target = this.checked;
    $("input[type='checkbox']").each(function(){
        this.checked = target; 
    });
});


$("#add_to_bid").click(function() {
    pendingArray = Array();
    $("input.checkbox").each(function() {
        if(this.checked) pendingArray.push($(this).attr("args"));
    });
});


$("#order_delete").click(function() {
    var id = $("#bid_modal").attr("args");
    if(confirm("是否确定删除？")) {
        Dajaxice.purchasing.newBidDelete(deleteCallBack, {"id": id});
        return true;
    }
    return false;
});
function deleteCallBack(data) {
    Dajaxice.purchasing.getOngoingBidList(getBidListCallBack, {});
}
