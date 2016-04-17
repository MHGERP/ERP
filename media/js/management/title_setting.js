$(document).ready(refresh);
$("#id_group").click(refresh);

function refresh() {
    var group_id = $("#id_group").val();
    var user_id = $("#widget-content").attr("user_id");
    Dajaxice.management.getTitleList(refreshCallBack, {"group_id": group_id, "setting_user": user_id});
}
function refreshCallBack(data) {
    $("#widget-content").html(data);
}

var touch;

$(document).on("click", ".btn-addorremove", function() {
    var title_id = $(this).parent().parent().attr("iid");
    var user_id = $("#widget-content").attr("user_id");
    var flag = $(this).hasClass("btn-success");
    touch = $(this);
    Dajaxice.management.addOrRemoveTitle(dealCallBack, {"title_id": title_id, user_id: user_id, "flag": flag});
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
