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

// $(document).on("click","#new_purchase_btn",function(){
//     newOrder();
// })

// function newOrder(){
// }