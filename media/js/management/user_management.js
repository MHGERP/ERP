$(document).ready(refresh);

function refresh() {
    Dajaxice.management.getUserList(getUserCallBack, {});
}
function getUserCallBack(data) {
    $("#widget-content").html(data);
}



$("#user-add").click(function() {
    $("#titleLabel").html("新建用户");

});

$("#user-save").click(function() {
    var user_name = $("#user_name").val();
    var user_password = $("#user_password").val();
    Dajaxice.management.createUser(refresh, {
                                                    "user_name": user_name,
                                                    "user_password": user_password,
                                                    
                                                    
                                            });
});