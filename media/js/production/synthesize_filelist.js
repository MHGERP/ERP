$(document).ready(refresh);

function refresh(){
	var id_work_order = $('#id_work_order').val();
	Dajaxice.production.getFileList(getFileListCallBack,{"id_work_order":id_work_order});
}
function getFileListCallBack(data){
	$('#widget-content').html(data);
}

$("#order_search").click(function(){
	refresh();
})

$(document).on("click",".confirm",function(){
    if(confirm("是否进行确认？")){
        var id = $(this).attr("id");
        var workorder_id = $(this).parent().parent().children(":first").html();
        Dajaxice.production.changeFileList(getFileListCallBack,{"id":id,"workorder_id":workorder_id});
    }
})
