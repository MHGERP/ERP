$(document).ready(function(){
 	refresh();
})

$(document).on("click","#btn_search",function(){
    refresh();
})

function refresh(){
    val = $("#id_inventory_type").val();
    key = $("#search_key").val();
    Dajaxice.purchasing.chooseInventorytype(choose_Inventorytype_callback,{
        "pid":val,  
        "key":key
    });
}

function choose_Inventorytype_callback(data){
    val = $("#id_inventory_type").val();
    item = $("#new_purchasing_order");
    $("#inventory_detail_table").html(data.inventory_detail_html);
    if(val==5){
        item.html(data.new_purchasing_form_html);
    }
    else{
        item.html(data.new_order_form_html);
    }
}

//五个表的详细记录删除
var cell;
$(document).on("click",".btn-danger",function(){
    cell = this;
    var uid = $(cell).attr("uid");
    if(confirm("确定删除吗？")){
            Dajaxice.purchasing.deleteDetail(delete_detail_callback,
                {"uid":uid}
            );
    }
 
})
function delete_detail_callback(data){
    $(cell).parent().parent().remove();
}

//新建订购单确认保存按钮
$(document).on("click","#save",function(){
    var num = $("#order_number").val();
    var cDate = $("#create_date").val();
    var eDate = $("#establishment_date").val();
    Dajaxice.purchasing.newOrderSave(save_callback,{
        "num":num,
        "cDate":cDate,
        "eDate":eDate
    });
})

function save_callback(){
    alert("该订购单已保存")
}

//新建订购单完成按钮
$(document).on("click","#finish",function(){
    var num = $("#order_number").val();
    var cDate = $("#create_date").val();
    var eDate = $("#establishment_date").val();
    if(confirm("确定后将不能再修改")){
        Dajaxice.purchasing.newOrderFinish(save_callback,{
            "num":num,
            "cDate":cDate,
            "eDate":eDate
        });
    }
})

$(document).on("click","#order_delete",function(){
    var num = $("#order_number").val();
    Dajaxice.purchasing.newOrderDelete(delete_callback,{
        "num":num,
    });
})

function delete_callback(){
    alert("该订购单已删除");
}