$(document).ready(refresh);
$("#id_auth_type").change(refresh);

function refresh() {
    var auth_type = $("#id_auth_type").val();
    var role_id = $("#widget-content").attr("role_id");
    Dajaxice.management.getControlList(refreshCallBack, {"auth_type": auth_type, "role_id": role_id});
}
function refreshCallBack(data) {
    $("#widget-content").html(data);
}

var touch;

$(document).on("click", ".btn-addorremove", function() {
    var perm_id = $(this).parent().parent().attr("iid");
    var role_id = $("#widget-content").attr("role_id");
    var flag = $(this).hasClass("btn-success");
    touch = $(this);
    Dajaxice.management.addOrRemoveAuth(dealCallBack, {"perm_id": perm_id, "role_id": role_id, "add": flag});
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
