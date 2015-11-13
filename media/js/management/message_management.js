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
    alert("caonimei");
    //$(#message_title).val("title");
    //$(#message_content).val("content");
}
