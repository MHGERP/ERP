$(document).ready(refresh);
$("#btn_search").click(refresh);

function refresh(){
    var statu = $("#id_status").val();
    var key = $("#search_key").val();
    Dajaxice.purchasing.getOrderFormList(getListCallBack, {"statu": statu, "key": key,})
}

function getListCallBack(data) {
    $("#widget-content").html(data);
}

$(document).on("click", ".btn-open", function() {
    index = $(this).attr("args"); 
    location.href = "/purchasing/orderForm?index=" + index;
});
$(document).on("click", ".btn-del", function() {
    index = $(this).attr("args"); 
    if(confirm("是否确定删除该订购单？"))
       Dajaxice.purchasing.deleteOrderForm(deleteCallBack, {"index": index, });
});
function deleteCallBack(data) {
    refresh();
}
$(document).on("click", ".btn-fns", function() {
    index = $(this).attr("args");
    if(confirm("是否确定终止该订购单？"))
        Dajaxice.purchasing.finishOrderForm(finishCallBack, {"index": index, });
});
function finishCallBack(data) {
    refresh();
}
