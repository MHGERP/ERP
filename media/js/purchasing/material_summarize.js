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

    Dajaxice.purchasing.getOngoingOrderList(getOrderListCallBack,{});
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

//delete five tables detail item
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

//new_purchase_btn
$(document).on("click","#new_purchase_btn",function(){
    Dajaxice.purchasing.newOrderCreate(newOrderCreateCallBack, {});
})

//open button
$(document).on("click","#btn-open",function(){
    var id = $(".search-query").val();
    Dajaxice.purchasing.getOrderForm(newOrderCreateCallBack,{"order_id":id,})
})

function newOrderCreateCallBack(data){
    $("input#order_number").val(data.order_id);
    $("div.table-div").html(data.html);
    $("#new_order_modal").attr("args", data.id);
    Dajaxice.purchasing.getOngoingOrderList(getOrderListCallBack,{});
}

function getOrderListCallBack(data) {
    $("#order-select").html(data);
}

//new puchase order save button
$("#btn-save").click(function() {
    var id = $("#bid_modal").attr("args");
    alert(id);
})

//new puchase order finish button
$(document).on("click","#finish",function(){
    var id = $("#bid_modal").attr("args");
    if(confirm("确定后将不能再修改")){
        Dajaxice.purchasing.newOrderFinish(finish_callback,{"id":id});
    }
})

function finish_callback(){
    alert("该订购单已创建完成，不能再修改");
}

//new puchase order delete button
$(document).on("click","#order_delete",function(){
    var num = $("#order_number").val();
    Dajaxice.purchasing.newOrderDelete(delete_callback,{
        "num":num,
    });
})

function delete_callback(){
    alert("该订购单已删除");
}

$(document).on("click", "input#selectall", function(){
    var target = this.checked;
    $("input[type='checkbox']").each(function(){
        this.checked = target; 
    });
});

//add_to_order button
// $(document).on("click","#add_to_order",function(){
//     Dajaxice.purchasing.getOngoingOrderList(addToOrderCallBack,{});
// })

function addToOrderCallBack(data){
    $("#order_select").html(data);
    items = $("#subcheck:checked").parent().parent().children();
    item = $(items[2]).text();
    alert(item);
    $("#order_select").change(function(){
        Dajaxice.purchasing.addToOrder(add_to_order_callback,{});
    })
}
