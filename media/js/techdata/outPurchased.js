$(document).ready(refresh);
$("#order_search").click(refresh);
function refresh(){
    var id_work_order = $("#id_work_order").val();
    var inventory_type = $("#order_search").attr("itype");
    Dajaxice.techdata.getInventoryTables(refreshCallBack, {"id_work_order": id_work_order, "inventory_type": inventory_type});
}

$("#fast_generate").click(function() {
    var id_work_order = $("#id_work_order").val();
    var inventory_type = $("#order_search").attr("itype");
    Dajaxice.techdata.autoSetInventoryLabel()
});

