$("#id_deadline").datetimepicker({

    weekStart:1,
    todayBtn: 1,
    autoclose: 1,
    todayHighlight:1,
    startView:2,
    forceParse:0,
    minView:0
});





var cid =""; /// for .addHomework .saveHomework
var error_list = new Array();
var hid = "";
function clearToColor(color)
{
    for(var i = 0; i < error_list.length; ++ i)
    {
        if(error_list == "") continue;
        cnt = "#id_"+error_list[i];
        $(cnt).css("background", color);
    }
}
//$(".addHomework").click(function()
$(document).on("click", ".addHomework", function()
{
    $('#homework_error').hide();
    $('#homework_modal_head').text("增加作业");
    clearToColor("white");

    cid = $(this).parents("[cid]").first().attr('cid');
    hid = ""
    $("#homework_modal").find("input").val("");
    $("#homework_modal").find("textarea").val("");
})


//$(".modifyHomework").click(function()
$(document).on("click", ".modifyHomework", function()
{
    $('#homework_error').hide();
    $('#homework_modal_head').text("修改作业");
    clearToColor("white");
    cid = $(this).parents("[cid]").first().attr('cid');
    var cnt = $(this).parents("tr");
    hid = $(this).attr('hid');
    $("input[name='name']").val($(cnt).children("td:eq(1)").text());
    $("textarea[name='required']").val($(cnt).children("td:eq(2)").text());
    $("input[name='deadline']").val($(cnt).children("td:eq(3)").text());



})

// $(".saveHomework").click(function()
$(document).on("click", ".saveHomework", function()
{    
    var form = $(this).parents(".modal").find("form").serialize();
    Dajaxice.common.saveHomework(saveHomeworkCallback, 
        {
            'form':form,
            'cid': cid,
            'hid': hid,
        });
})
function saveHomeworkCallback(data)
{
    if(data.status == 0)
    {
        $('#homework_error').hide();
        $('#homework_modal').modal("hide");
        var cnt = $("[cid="+cid+"]");
        cnt.find("table").remove();
        cnt.append(data.homework_table);
    }
    else if(data.status == 1)
    {
        $('#homework_error').html("<h3> "+"您有字段未填写或填写错误"+"</h3>");
        error_list = data.error_list.split(",");
        clearToColor("red");
        $('#homework_error').show(500);
    }
}


$(document).on("click", ".viewHomeworkSubmit", function()
{
    $("#homework_page").hide();
    $("#homework_submit_page").show();
    Dajaxice.common.getHomeworkSubmitList(getHomeworkSubmitListCallback, 
        {
            'hid': $(this).attr("hid"),
        });
    

})
function getHomeworkSubmitListCallback(data)
{
    $("#homework_submit_page").append(data.homework_submit_table);
}
$(document).on("click", "#return", function()
{  
    $("#homework_submit_table").remove();
    
    $("#homework_submit_page").hide();
    $("#homework_page").show();


})