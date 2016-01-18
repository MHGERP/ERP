$(document).on("click",".check",function(){
	if(confirm("确定进行确认吗？"))
		$(this).addClass("btn-primary");
})