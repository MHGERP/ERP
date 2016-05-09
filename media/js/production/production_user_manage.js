$(document).ready(refresh);

function refresh(){
    Dajaxice.production.getProductionUser(getProductionUserCallBack,{"form":$("#productionUserSearchForm").serialize()});
}

$(document).on("click","#searchUser",function(){
    refresh();
})

function getProductionUserCallBack(data){
    $("#productionUserTable").html(data);
}

$(document).on("click","#addUser",function(){
    $("#add_production_user_modal").modal("show");
    searchUser();
    //Dajaxice.production.addProductionUser(addProductionUserCallBack,{"form":$("#productionUserSearchForm").serialize()});
})

$(document).on("click","#user_search_btn",searchUser);

function searchUser(){
    Dajaxice.production.getUser(getUserCallBack,{"form":$("#user_choice_form").serialize()});
}

function getUserCallBack(data){
    $("#UserTable").html(data);
}
// function addProductionUserCallBack(data){

//     $("#message").innerHTML = data;
// }