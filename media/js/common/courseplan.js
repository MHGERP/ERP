var mod;
$("#add_new_courseplan").click(function(){
    $(".errorlist").remove();
    $("#id_course_plan_id").val('');
    $("#id_course_name").val('');
    $('#id_course_grade option:first').attr('selected','selected');
    $('#id_course_term option:first').attr('selected','selected');
    $("#id_course_point").val('');
    mod=-1;

});

$(document).on("click","#change_course_plan",function(){
    tr=$(this).closest("tr");
    $(".errorlist").remove();
    var iid=$(tr).children("td:eq(0)").html();
    $("#id_course_plan_id").val($(tr).children("td:eq(0)").html());
    $("#id_course_name").val($(tr).children("td:eq(1)").html());
    $("#id_course_grade").val($(tr).children("td:eq(2)").text());
    $("#id_course_term").val($(tr).children("td:eq(3)").text());
    $("#id_course_point").val($(tr).children("td:eq(4)").html());
    mod=$(tr).attr("iid");

});
$(document).on("click","#delete_course_plan",function(){
    tr=$(this).closest("tr");
    mod=$(tr).attr("iid");
});
$("#delete_confirm").click(function(){
    var val;   
    if($("#PracticeSelect").length>0){
        val=$("#PracticeSelect").val();
    }
    else{
        val=-1;
    }
    Dajaxice.common.CoursePlanDelete(add_or_update_callback,{
        "iid":mod,
        "pid":val
    });
});
$(document).on("click","#add_or_update_courseplan",function(){
    var val;   
    if($("#PracticeSelect").length>0){
        val=$("#PracticeSelect").val();
    }
    else{
        val=-1;
    }
    Dajaxice.common.CoursePlanChange(add_or_update_callback,{
        "courseplanform":$("#course_plan_info_form").serialize(true),
        "iid":mod,
        "pid":val
    });
});
function add_or_update_callback(data){
    if(data.status===0)
    {
        $("#course_plan_modal").modal('hide');
        $("#course_plan_table").html(data.courseplan_html);
    }
    else{
        $("#course_plan_info_form").html(data.error_list);
    }
}
$("#PracticeSelect").change(function(){
    val=$("#PracticeSelect").val();
    if(val==-1){
        location.reload(true);
    }
    else{
        Dajaxice.adminStaff.ChosePractice(chose_practice_callback,{
            "pid":val
        });
    }
});
function chose_practice_callback(data){
    $("#course_plan_table").html(data.courseplan_html);
    $("#add_new_courseplan").attr("disabled",false);
}
$(document).ready(function(){
    if($("#PracticeSelect").length>0)
    {
        $("#add_new_courseplan").attr("disabled",true);
    }
});
