$("#update-user").click(function(){
    Dajaxice.home.updateUserInfo(updateUserInfoCallback,{
        "user_form":$("#user_info_form").serialize(true),
    });
});

function updateUserInfoCallback(data){
    alert(data);
}

$("#user-info").click(function(){
    Dajaxice.home.getUserInfoForm(getUserInfoFormCallback,{});
})

function getUserInfoFormCallback(data){
    $("#modal-userinfo-event .modal-body").html(data); 
}
/*BinWu begin here*/
$("#mymessage_box").click(function() {
    Dajaxice.management.getBoxList(getBoxListCallBack, {});
});

function getBoxListCallBack(data) {
    $("#check_mymessage").html(data);
    $("#check_mymessage").modal('show'); 
}

$(document).on("click", ".warning, .success", function() {
    var box = $(this).attr("bid");
    $(this).removeClass();
    $(this).addClass("success");
    Dajaxice.management.checkBox(checkBoxCallBack, {"boxId": box});
});

function checkBoxCallBack(data) {
    $("#box_title").html("标题：<b>" + data.message_title + "</b>");
    $("#box_content").html("内容：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + data.message_content);
    if (data.filepath.length > 0) 
        {
            html = "<p>附件：</p>" + "<table class='table table-bordered table-striped' style='width: 60%;'>";
            for (i = 0; i < data.filepath.length; i++) {
                html += "<tr>" +
                            "<td>" + data.filename[i]  + "</td>" +
                            "<td>" +"<a class='btn btn-warning btn-small' href='"+ data.filepath[i] + "'>下载</a></td>" +
                        "</tr>";
            }
        }
        else {
            html = "";
        }
        html += "</table>";
        $("#box_download").html(html);
}
/*BinWu end here*/
