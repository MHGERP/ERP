$(document).ready(refresh);

function refresh() {
    var index = $("#index").val();
    Dajaxice.purchasing.getOrderFormItems(getItemsCallBack, {
        "index": index,
    });
}
function getItemsCallBack(data) {
    $("#item_table").html(data);
}


$("#btn-open").click(function() {
   var bid_id = $(".search-query").val();
   Dajaxice.purchasing.getBidForm(getBidCallBack, {"bid_id": bid_id,})
});

$("#new_purchase_btn").click(function() {
    Dajaxice.purchasing.newBidCreate(getBidCallBack, {});
});

function getBidCallBack(data) {
    $("input#bid_id").val(data.bid_id);
    $("div.table-div").html(data.html);
}
