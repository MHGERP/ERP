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

$(document).on("click",".check",function(){
	if(confirm("确定进行确认吗？"))
		$(this).addClass("btn-primary");
})