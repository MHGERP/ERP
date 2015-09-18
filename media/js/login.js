$(":radio").click(function(){
    var val=$(this).val();
    $("#loginform").attr("action","/?next=/loginredirect/"+val+"/");
});
$(document).ready(function(){
	$("#id_username").addClass("form-control");
	$("#id_username").attr("placeholder","用户名");
	$("#id_password").addClass("form-control");
	$("#id_password").attr("placeholder","密码");
	$("button").css("width","170px");
	$("label").css("margin","0px 4px");
	$(".input-group").css("width","75%");
});


var u_agent=(navigator.userAgent);
if(u_agent.indexOf("Safari")>-1||u_agent.indexOf("Firefox")>-1||window.opera){}
else if(u_agent.indexOf("MSIE")>0&&!window.innerWidth){
    //document.location.reload(true);
    window.open("http://202.118.67.200:2000");
    window.opener=null;
    window.open('','_self'); 
    window.close();
}
