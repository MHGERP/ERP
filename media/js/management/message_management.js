$(document).ready(refresh);
function refresh() {
    var loguser = $("#loguser").text();
    Dajaxice.management.getMessageList(getMessageListCallBack, {"loguser": loguser});
}
function getMessageListCallBack(data) {
    $("#widget-content").html(data);
}

$(document).on("click", ".btn-delete", function() {
    var message = $(this).parent().parent().attr("iid");
    if (confirm("确定撤销？")) {
        Dajaxice.management.deleteMessage(deleteMessageCallBack, {"messageId": message});
    }
});
function deleteMessageCallBack(data) {
    refresh();
}

$(document).on("click", "#message_send", function() {
    document.getElementById('message_form').submit();
});

$(document).on("click", ".btn-change-name", function() {
    var message = $(this).parent().parent().attr("iid");
    Dajaxice.management.checkMessage(checkMessageCallBack, {"messageId": message});
});

function checkMessageCallBack(data) {
    $("#check_title").html("标题：<b>" + data.message_title + "</b>");
    $("#check_content").html("内容：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + data.message_content);
    if (data.filepath.length > 0) 
    {
        html = "<p>附件：</p>" + "<table class='table table-bordered table-striped' style='width: 60%;'>";
        for (i = 0; i < data.filepath.length; i++) {
            html += "<tr>" +
                        "<td>" + data.filename[i]  + "</td>" +
                        "<td>" +
                            "<a class='btn btn-warning btn-small' href='"
                                + data.filepath[i] + "'>下载</a></td>" +
                    "</tr>";
        }
    }
    else {
        html = "";
    }
    html += "</table>";
    $("#check_download").html(html);
}
