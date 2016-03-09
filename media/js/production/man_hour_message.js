$(document).ready(refresh);
function refresh(){
    id_work_order = $("#id_order_index").val();
    work_ticket = $("#id_work_ticket").val();
    group_num = $("#id_group_num").val();
    Dajaxice.production.getHourSearch(getHourSearchCallBack,{
        "id_work_order":id_work_order,
        "work_ticket":work_ticket,
        "group_num":group_num
    });
}
$(document).on("click","#btn-search",function(){
    refresh();
})

function getHourSearchCallBack(data){
    $("#widget-content").html(data);
}