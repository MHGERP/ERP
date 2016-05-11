$("#id_complete_date__gte").datetimepicker({
    format : 'yyyy-mm-dd',
    minView : 2,
    autoclose : true,
});

$("#id_complete_date__lte").datetimepicker({
  format : 'yyyy-mm-dd',
  minView : 2,
  autoclose : true,
});

$(document).ready(refresh);

function refresh(){
    Dajaxice.production.getHourSummarize(getHourSummarizeCallBack,{"form":$("#hourSummarizeForm").serialize()});
}
$(document).on("click","#btn-search",function(){
    refresh();
})

function getHourSummarizeCallBack(data){
    $("#widget-content").html(data);   
}

$(document).on("click","#summarize-ticket",function(){
    tr = $(this).parent().parent();
    work_order_id = $(tr).find("td:eq(0)").attr("uid");
    groupNumId = $(tr).find("td:eq(1)").attr("uid");
    date = $(tr).find("td:eq(2)").html();
    Dajaxice.production.getSummarizeTicket(getHourTableCallBack,{
        "work_order_id":work_order_id,
        "groupNumId":groupNumId,
        "date":date
    });
})

function getHourTableCallBack(data){
    $("#summarize_ticket_modal").modal();
    $("#summarize-ticket-table").html(data);
}

$(document).on("click","#part-ticket",function(){
    tr = $(this).parent().parent();
    work_order_id = $(tr).find("td:eq(0)").attr("uid");
    groupNumId = $(tr).find("td:eq(1)").attr("uid");
    date = $(tr).find("td:eq(2)").html();
    Dajaxice.production.getPartTicket(getPartTicketCallBack,{
        "work_order_id":work_order_id,
        "groupNumId":groupNumId,
        "date":date
    });
})

function getPartTicketCallBack(data){
    $("#part_ticket_modal").modal();
    $("#part-ticket-table").html(data);

}