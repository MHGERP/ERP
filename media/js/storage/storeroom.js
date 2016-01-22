function clear(){
    $("[name = name]").val("");
    $("[name = position]").val("");
    $("[name = material_type]").val("");
}

var sr_id;
$(document).ready(function() {
    $("#searchSR").click(function(){
        Dajaxice.storage.storeRoomSearch(storeRoomSearchCallBack, {"form":$("#sr_searchForm").serialize()});
    });
    $("#insertSR").click(function(){
        clear();
        $("#srSave").attr("mark","insert");
        $(".modal-header h3").html("添加库房记录");
        $("#sr_form")[0].reset();
    });
    $("#updateSR").live('click',function(){
        $("#srSave").attr("mark", "update");
        $(".modal-header h3").html("修改库房记录");
        sr_id = $(this).parents("tr").attr("sr_id");
        temp = $(document).find("tr[sr_id="+sr_id+"]");
        name = temp.children().eq(0).text();
        position = temp.children().eq(1).text();
        material_type = temp.children().eq(2).attr("mt");
        alert(name + ", " + position + ", " + material_type);
        $("#sr_form")[0].reset();
        //$(document).getElementById("#sr_form").reset();
        $("#sr_form").find("[name=name]").val(name);
        $("#sr_form").find("[name=position]").val(position);
        $("#sr_form").find("[name=material_type]").val(material_type);
    });
    $("#srSave").click(function() {
        if($(this).attr("mark") == "insert"){
            alert("kad");
            Dajaxice.storage.storeRoomAdd(storeRoomAddCallBack, {"form": $("#sr_form").serialize()});
        }else if($(this).attr("mark") == "update"){
            alert(sr_id);
            Dajaxice.storage.storeRoomUpdate(storeRoomUpdateCallBack, {"form":$("#sr_form").serialize(),"sr_id":sr_id});
        }
    });
    $("#deleteSR").live('click',function(){
        var temp = confirm("删除不可恢复！");
        if(temp === true){
            sr_id = $(this).parents("tr").attr("sr_id");
            Dajaxice.storage.storeRoomDelete(storeRoomDeleteCallBack, {"sr_id":sr_id});
        }       
    });
});

function storeRoomSearchCallBack(data){
    $("#room_table").html(data.html);
}

function storeRoomAddCallBack(data) {
    if(data.flag){
        alert(data.message);
        $("#room_table").html(data.html);
        $("#myModal").modal('hide');
    }else{
        alert(data.message);
        $("#myModal").modal('hide');
    }
}

function storeRoomUpdateCallBack(data){
    if(data.flag){
        alert(data.message);
        $("#room_table").html(data.html);
        $("#myModal").modal('hide');
    }else{
        alert(data.message);
        $("#myModal").modal('hide');
    }
}

function storeRoomDeleteCallBack(data){
    if(data.flag){
        alert(data.message);
        $(document).find("tr[sr_id = "+data.sr_id+"]").remove();
    }
}
