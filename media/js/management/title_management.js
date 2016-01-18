$(document).ready(refresh);
$("#id_group").change(refresh);

function refresh() {
    var group_id = $("#id_group").val();
    Dajaxice.management.getTitleList(getTitleCallBack, {"group_id": group_id});
}
function getTitleCallBack(data) {
    $("#widget-content").html(data);
}

var title_id;

$("#btn-add").click(function() {
    $("#titleLabel").html("新建头衔");
    title_id = "-1";
});
$(document).on("click", ".btn-change-name", function() {
    $("#titleLabel").html("修改头衔名");
    title_id = $(this).parent().parent().attr("iid");
});


$("#btn-save").click(function() {
    var group_id = $("#id_group").val();
    var title_name = $("#title-name").val();
    Dajaxice.management.createOrModifyTitle(refresh, {
                                                    "group_id": group_id,
                                                    "title_name": title_name,
                                                    "title_id": title_id,
                                            });
});


$(document).on("click", ".btn-delete", function() {
    title_id = $(this).parent().parent().attr("iid");
    if(confirm("你确定删除该头衔？")) {
        Dajaxice.management.deleteTitle(refresh, {"title_id": title_id});
    }
});


$(document).on("click", '.btn-query-authority', function() {
    title_id = $(this).parent().parent().attr("iid");
    location.href = "/management/authorityManagement?title_id=" + title_id;
});
