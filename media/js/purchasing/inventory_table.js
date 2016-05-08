$(document).ready(refresh);

function getTableCallBack(data) {
    $(".widget-content").html(data);
}

function refresh() {
    var table_id = $(".widget-content").attr("tableid");
    var order_index = $(".widget-content").attr("order_index");
    Dajaxice.purchasing.getInventoryTable(getTableCallBack, {"table_id": table_id, "order_index": order_index,})
}

$(document).on("click", ".btn-add_to_detail-all", function() {
    var table_id = $(".widget-content").attr("tableid");
    var order_index = $(".widget-content").attr("order_index");
    Dajaxice.purchasing.addToDetail(addCallBack, {"table_id": table_id, "order_index": order_index, })
});

var index;
$(document).on("click", ".btn-add_to_detail", function() {
   index = $(this).attr("args");
   Dajaxice.purchasing.addToDetailSingle(addCallBack, {"index": index, });
});

$(document).on("click", ".btn-add_to_foreign", function() {
  index = $(this).attr("args1");
  //alert(index);
  Dajaxice.purchasing.addToForeign(addCallBack, {"index": index, });
});

function addCallBack(data) {
    refresh();
}
