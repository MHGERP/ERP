$(document).ready(refresh);

function refresh() {
    Dajaxice.management.getGroupList(getGroupCallBack, {});
}
function getGroupCallBack(data) {
    $("#widget-content").html(data);
}

var group_id;

$("#add_group").click(function() {
    group_id = "-1";
    $("#groupLabel").html("添加部门"); 
});
$(document).on("click", ".btn-change-name", function() {
    group_id = $(this).parent().parent().attr("iid");
    $("#groupLabel").html("修改部门名"); 
});
$("#btn-finish").click(function() {
    var name = $("#new_group_name").val();
    Dajaxice.management.createOrModifyGroup(refresh, {"name": name, "group_id": group_id, }); 
});

$(document).on("click", ".btn-delete", function() {
     var id = $(this).parent().parent().attr("iid");
     if(confirm("您确定删除该部门？"))
         Dajaxice.management.deleteGroup(deleteCallBack, {"id": id});
});
function deleteCallBack(data) {
    if(data == "ok") {
        alert("删除成功！");
        refresh();
    }
    else {
        alert("删除失败！");
    }
}

var pending_group_id;

$(document).on("click", ".btn-add-admin", function() {
    $("#adminLabel").html("添加管理员");  
    pending_group_id = $(this).parent().parent().attr("iid");
});
$(document).on("click", ".btn-change-admin", function() {
    $("#adminLabel").html("修改管理员");    
    pending_group_id = $(this).parent().parent().attr("iid");
});



$("#btn-candidate-search").click(function() {
    var val = $("#candidate-name").val(); 
    Dajaxice.management.searchCandidate(searchCallBack, {"key": val});
});
function searchCallBack(data) {
    $("#candidate-div").html(data);
}

$("#btn-select-candidate").click(function() {
    var id = $("input:radio:checked").val();
    if(confirm("你确定添加该用户为新群组管理员？")) {
        Dajaxice.management.addAdmin(refresh, {"group_id": pending_group_id,
                                                    "user_id": id,})
        return true;
    }
    return false;
});
