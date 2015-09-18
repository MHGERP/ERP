$("#next_term_confirm").click(function(){
    var start=$("#first_day").val();
    Dajaxice.adminStaff.GoNextTerm(settingCallBack,{
        "first":start    
    });
});

function settingCallBack(data){
    alert("操作成功");
    location.reload(true);
}
$("#first_day").datetimepicker({
    format:'yyyy-mm-dd',
    weekStart:1,
    todayBtn: 1,
    autoclose: 1,
    todayHighlight:1,
    startView:2,
    forceParse:0,
    minView:2

});
$("#course_start").datetimepicker({
    format:'yyyy-mm-dd hh:ii',
    weekStart:1,
    todayBtn: 1,
    autoclose: 1,
    todayHighlight:1,
    startView:2,
    forceParse:0,
    minView:0

});
$("#course_end").datetimepicker({
    format:'yyyy-mm-dd hh:ii',
    weekStart:1,
    todayBtn: 1,
    autoclose: 1,
    todayHighlight:1,
    startView:2,
    forceParse:0,
    minView:0

});
$("#score_start").datetimepicker({
    format:'yyyy-mm-dd hh:ii',
    weekStart:1,
    todayBtn: 1,
    autoclose: 1,
    todayHighlight:1,
    startView:2,
    forceParse:0,
    minView:0

});
$("#score_end").datetimepicker({
    format:'yyyy-mm-dd hh:ii',
    weekStart:1,
    todayBtn: 1,
    autoclose: 1,
    todayHighlight:1,
    startView:2,
    forceParse:0,
    minView:0

});
$("#course_time_confirm").click(function(){
    var start=$("#course_start").val();
    var end=$("#course_end").val();
    Dajaxice.adminStaff.SetCourseTime(settingCallBack,{
       "start":start,
       "end":end
    });
});
$("#score_time_confirm").click(function(){
    var start=$("#score_start").val();
    var end=$("#score_end").val();
    Dajaxice.adminStaff.SetScoreTime(settingCallBack,{
       "start":start,
       "end":end
    });
});
