$("#sc_button").click(function(){
    var sid=$("#studentid").val();
    Dajaxice.common.GetCourseInfo(get_course_callback,{
        'sid':sid
    });
});
function get_course_callback(data){
    $("#select_course_div").html(data.select_table_html);
};
