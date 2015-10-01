$(document).ready(function() {
    var table_id = $(".widget-content").attr("tableid");
    var order_index = $(".widget-content").attr("order_index");
    Dajaxice.purchasing.getInventoryTable(getTableCallBack, {"table_id": table_id, "order_index": order_index,})
})
function getTableCallBack(data) {
    $(".widget-content").html(data);
}
