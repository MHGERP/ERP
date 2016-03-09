$(document).ready(refresh);
function refresh(){
    work_order = $("#id_order_index").val();
    name = $("#id_operator").val();
    date = $("#id_date").val();
    Dajaxice.production.getHourSummarize(getHourSummarizeCallBack,{
        "work_order":work_order,
        "operator":name,
        "date":date
    });
}
$(document).on("click","#btn-search",function(){
    refresh();
})

function getHourSummarizeCallBack(data){
    if(data.status==0)
        alert(data.message);
    else
        $("#widget-content").html(data.html);   
}

$(document).on("click","#summarize-ticket",function(){
    tr = $(this).parent().parent();
    work_order = $(tr).find("td:eq(0)").html();
    operator = $(tr).find("td:eq(1)").html();
    date = $(tr).find("td:eq(2)").html();
    Dajaxice.production.getSummarizeTicket(getHourTableCallBack,{
        "work_order":work_order,
        "operator":operator,
        "date":date
    });
})

function getHourTableCallBack(data){
    if(data.status==0)
        alert(data.message);
    else
        $("#summarize_ticket_modal").modal();
        $("#summarize-ticket-table").html(data.html);
}

$(document).on("click","#part-ticket",function(){
    tr = $(this).parent().parent();
    work_order = $(tr).find("td:eq(0)").html();
    operator = $(tr).find("td:eq(1)").html();
    date = $(tr).find("td:eq(2)").html();
    Dajaxice.production.getPartTicket(getPartTicketCallBack,{
        "work_order":work_order,
        "operator":operator,
        "date":date
    });
})

function getPartTicketCallBack(data){
    if(data.status==0)
        alert(data.message);
    else
        $("#part_ticket_modal").modal();
        $("#part-ticket-table").html(data.html);

}