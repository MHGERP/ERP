$("#sc_button").click(function(){
    var sid=$("#studentid").val();
    Dajaxice.common.GetDeleteCourseInfo(get_delete_course_callback,{
        'sid':sid
    });
});
function get_delete_course_callback(data){
    $("#delete_course_div").html(data.delete_table_html);
};
