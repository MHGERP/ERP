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
    $("#bid-select").html(data);
}
function getItemsCallBack(data) {
    $("#item_table").html(data);
}

$("#btn-save").click(function() {
    var id = $("#bid_modal").attr("args");
    alert(id);
})
$("#btn-finish").click(function() {
    var id = $("#bid_modal").attr("args");
    Dajaxice.purchasing.newBidFinish(finishCallBack, {"id": id});
})
function finishCallBack() {

}

$("#btn-open").click(function() {
   var id = $(".search-query").val(); // datatable index not bid_id
   Dajaxice.purchasing.getBidForm(getBidCallBack, {"bid_id": id,})
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
