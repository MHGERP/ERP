$(document).on("change","#ClassRoom",function(){
    val=$("#ClassRoom").val();
    if(val==-1)
    {
        location.reload(true);
    }
    else{
        Dajaxice.adminStaff.ChoseRoom(choseroomcallback,{
            "rid":val
        });
    }
});

function choseroomcallback(data){
    $("#classroom_table").html(data.roomhtml);
    var room=$("#ClassRoom").find("option:selected").text();
    $("h2").html(room+"教室课程表");
}


$(document).on("click","#print_confirm",function(){
    var bodyhtml=$("body").html();
    $("body").css("background-image","none");
    $("body").html($("#classroom_table").html());
    print();
    $("body").css("background-image","url(/static/images/background.jpg)");
    $("body").html(bodyhtml);

});

function add_classRoom(){
    $('#classRoomadd_error_message').empty();
    Dajaxice.adminStaff.AddClassRoom(add_classroom_callback,
                                  {'form':$('#classRoomAddForm').serialize(true)});
}

function add_classroom_callback(data){
    $('#classRoomadd_error_message').append("<strong>"+data.message+"</strong>");
}