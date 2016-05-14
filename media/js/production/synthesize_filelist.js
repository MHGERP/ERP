$(document).ready(refresh);

function refresh(){
	Dajaxice.production.getFileList(getFileListCallBack,{"form":$("#subWorkOrderForm").serialize()});
}
function getFileListCallBack(data){
	$("#widget-content").html(data);
}

$("#order_search").click(function(){
	refresh();
})

$(document).on("click",".confirm",function(){
    if(confirm("是否进行确认？")){
        var status = $(this).attr("uid");
        var workorder_id = $(this).parent().parent().attr("uid");
        Dajaxice.production.changeFileList(changeFileListCallBack,{"status":status,"workorder_id":workorder_id,"is_check":true});
    }
})

$(document).on("click",".back",function(){
    if(confirm("是否进行撤消？")){
        var status = $(this).attr("uid");
        var workorder_id = $(this).parent().parent().attr("uid");
        Dajaxice.production.changeFileList(changeFileListCallBack,{"status":status,"workorder_id":workorder_id,"is_check":false});
    }
})

function changeFileListCallBack(){
    refresh();
}
