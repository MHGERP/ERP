$(document).ready(refresh);

function refresh(){
    Dajaxice.production.getProductionUser(getProductionUserCallBack,{"form":$("#productionUserSearchForm").serialize()});
}

$(document).on("click","#searchProductionUser",function(){
    refresh();
});

function getProductionUserCallBack(data){
    $("#productionUserTable").html(data);
}

$(document).on("click","#addUser",function(){
    $("#add_production_user_modal").modal("show");
    searchUser();
});

$(document).on("click","#user_search_btn",searchUser);

function searchUser(){
    Dajaxice.production.getUser(getUserCallBack,{"form":$("#user_choice_form").serialize()});
}

function getUserCallBack(data){
    $("#UserTable").html(data);
}

$(document).on("click","#user-save",function(){
    var userAllList = $("#select_table tbody").children("tr");
    var checkUserList = new Array();
    $(userAllList).each(function(i){
        var tt = $(this).find("td:eq(0)").children().eq(0);
        if(tt.attr("checked")==="checked"){
            checkUserList.push($(this).children("td").eq(1).text());
        }
    });
    Dajaxice.production.addProdUser(addProdUserCallBack,{"checkUserList":checkUserList});
});

function addProdUserCallBack(){
    $("#add_production_user_modal").modal("hide");
    alert("添加成功");
    refresh();
}

var produserid = ""

$(document).on("click","#produser_modify_btn",function(){
    produserid = $(this).parents("tr").attr("uid");
    Dajaxice.production.prodUserModify(modifyProductionUserCallBack, {"produserid": produserid});
});

function modifyProductionUserCallBack(data){
    $("#productionplan_update_div").html(data);
    $("#production_user_modify_modal").modal("show");
}

$(document).on("click","#prouser_modify_confirm_btn",function(){
    Dajaxice.production.saveProdUserModify(saveProdUserModifyCallBack,{"form":$("#productionplan_update_form").serialize(),"produserid":produserid})
});

function saveProdUserModifyCallBack(data){
    $("#production_user_modify_modal").modal("hide");
    refresh();
    alert(data);
}

$(document).on("click", "#produser_delete_btn", function(){
  temp = confirm("删除不可恢复");
  if(temp == true){
    uid = $(this).parents("tr").attr("uid");
    Dajaxice.production.prodUserDelete(prodUserDeleteCallBack, {"uid":uid});
  }
});

function prodUserDeleteCallBack(data){
  $(document).find("tr[uid="+ data +"]").remove();
}

