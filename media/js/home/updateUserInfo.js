$("#update-user").click(function(){
    Dajaxice.home.updateUserInfo(updateUserInfoCallback,{
        "user_form":$("#user_info_form").serialize(true),
    });
});

function updateUserInfoCallback(data){
    alert(data);
}

$("#user-info").click(function(){
    Dajaxice.home.getUserInfoForm(getUserInfoFormCallback,{});
})

function getUserInfoFormCallback(data){
    $("#modal-userinfo-event .modal-body").html(data); 
}