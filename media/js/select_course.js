$(document).on("click","#select_confirm",function(){
    var select_div = $("#select_course");
    var box = $(select_div).find(".course_checkbox");
    var selected=new Array();
    for(var i=0;i<box.length;++i)
    {
        if(box[i].checked)
        {
            var val=box[i].parentNode.parentNode.getAttribute("iid");
            selected.push(val);
        }
    
    }
    
    if(selected.length===0)
    {
        $("#info_alert").html("没有选定课程！");
        $("#alert_info_modal").modal('show');
        return false;
    }
    var sid=-1;
    if($("#studentid").length>0)
    {
        sid=$("#studentid").val();
    }
    Dajaxice.common.SelectCourseOperation(select_course_callback,{
        "selected":selected,
        "sid":sid
    })
});

function select_course_callback(data){

        $("#info_alert").html(data.status);
        $("#alert_info_modal").modal('show');

}
$(document).on("hide.bs.modal","#alert_info_modal",function(e){
    
    location.reload(true);   
});
