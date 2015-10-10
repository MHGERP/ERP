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
