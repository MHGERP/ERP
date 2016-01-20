$(document).ready(refresh);
function refresh(){
    id_work_order = $("#id_order_index").val();
    work_ticket = $("#work-ticket").val();
    group_num = $("#group-num").val();
    Dajaxice.production.getHourSummarize(getHourSummarizeCallBack,{
        "id_work_order":id_work_order,
        "work_ticket":work_ticket,
        "group_num":group_num
    });
}
$(document).on("click","#btn-search",function(){
    refresh();
})

function getHourSummarizeCallBack(data){
    $("#widget-content").html(data);
}