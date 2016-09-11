$(document).ready(refresh);
$("#id_group").change(refresh);

function refresh() {
    var group_id = $("#id_group").val();
    Dajaxice.management.getTitleList(getTitleCallBack, {"group_id": group_id});
}
function getTitleCallBack(data) {
    $("#widget-content").html(data);
}

var role_id;

$("#btn-add").click(function() {
    $("#titleLabel").html("新建头衔");
    role_id = "-1";
});
$(document).on("click", ".btn-change-name", function() {
    $("#titleLabel").html("修改头衔名");
    role_id = $(this).parent().parent().attr("iid");
});


$("#btn-save").click(function() {
    var group_id = $("#id_group").val();
    var role_name = $("#title-name").val();
    Dajaxice.management.createOrModifyTitle(refresh, {
                                                    "group_id": group_id,
                                                    "role_name": role_name,
                                                    "role_id": role_id,
                                            });
});


$(document).on("click", ".btn-delete", function() {
    role_id = $(this).parent().parent().attr("iid");
    if(confirm("你确定删除该头衔？")) {
        Dajaxice.management.deleteTitle(refresh, {"role_id": role_id});
    }
});


$(document).on("click", '.btn-query-authority', function() {
    role_id = $(this).parent().parent().attr("iid");
    location.href = "/management/controlManagement?role_id=" + role_id;
});
