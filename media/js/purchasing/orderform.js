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
