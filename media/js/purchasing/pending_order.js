$(document).ready(refresh)
$("#order_search").click(refresh)

function refresh() {
    var key = $("#search_key").val();
    Dajaxice.purchasing.pendingOrderSearch(searchCallBack, {"order_index": key});
}
function searchCallBack(data) {
    $("div.widget-content").html(data);
}

$(document).on("click", ".inventory_open", function(){
    var order_index = $(this).attr("args");
    var tem = $(this).parent().children().get(0);
    var tableid = $(tem).val();
    location.href = "/purchasing/inventoryTable?order_index=" + order_index + "&tableid=" + tableid;
});

function order_finish(id){
    Dajaxice.purchasing.SubOrderFinish(function(data){
        window.location.reload();
    },{
        'workorder_id':id
    });
}
