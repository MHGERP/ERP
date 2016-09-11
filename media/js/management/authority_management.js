$(document).ready(refresh);

function refresh() {
    Dajaxice.management.getAuthList(refreshCallBack);
}
function refreshCallBack(data) {
    $("#widget-content").html(data);
}

var touch;

$(document).on("click", ".btn-delete", function() {
    touch = $(this);
});
function dealCallBack(data) {
    if(data == "ok") {
        if(touch.hasClass("btn-success")) touch.removeClass("btn-success").addClass("btn-warning").html("取消");
        else touch.removeClass("btn-warning").addClass("btn-success").html("添加");
    }
    else {
        alert("fatal error!");
    }
}
