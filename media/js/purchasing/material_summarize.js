var pendingArray = Array();

$(document).ready(function(){
 	refresh();
});

$(document).on("click","#btn_search",function(){
    refresh();
});

function refresh(){
    $("#add_to_bid").hide();
    $("#add_to_order").hide();
    val = $("#id_inventory_type").val();
    key = $("#search_key").val();
    Dajaxice.purchasing.chooseInventorytype(choose_Inventorytype_callback,{
        "pid":val,  
        "key":key
    });
}

function getOrderListCallBack(data) {
    $(".order-select").each(function(){
        $(this).html(data);
    })
}

function choose_Inventorytype_callback(data){
    val = $("#id_inventory_type").val();
    item = $("#new_purchasing_order");
    $("#inventory_detail_table").html(data.inventory_detail_html);
    if(val==5){
        item.html(data.new_purchasing_form_html);
        $("#add_to_bid").show();
        $("#add_to_order").hide();
        Dajaxice.purchasing.getOngoingBidList(getBidListCallBack, {});
    }
    else{
        item.html(data.new_order_form_html);
        $("#add_to_order").show();
        $("#add_to_bid").hide();
        Dajaxice.purchasing.getOngoingOrderList(getOrderListCallBack,{});
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
 
});
function delete_detail_callback(data){
    $(cell).parent().parent().remove();
}

//new purchase order save button
$(document).on("click","#btn-save",function(){
    var id = $("#new_order_modal").attr("args");
    if(confirm("是否确认保存？")) {
        Dajaxice.purchasing.newOrderSave(saveCallBack, {"id": id, "pendingArray": pendingArray, });
    }
});
function saveCallBack() {
    alert("保存成功");
}

//new puchase order finish button
$(document).on("click","#btn-finish",function(){
    var id = $("#new_order_modal").attr("args");
    if(confirm("是否确认完成编制？")){
        Dajaxice.purchasing.newOrderFinish(finishCallBack,{"id":id});
    }
});
function finishCallBack() {
    alert("编制成功");
}

//open button
$(document).on("click",".btn-open",function(){
    if($(this).hasClass("clear")) {
        pendingArray = Array();
    }
    var id = $($(this).attr("data-source")).val();
    Dajaxice.purchasing.getOrderForm(getOrderCallBack,{"order_id":id,"pendingArray":pendingArray,})
});

//new purchase button
$(document).on("click","#new_purchase_btn",function(){
    Dajaxice.purchasing.newOrderCreate(getOrderCallBack, {});
});

function getOrderCallBack(data){
    $("input#order_number").val(data.order_id);
    $("div.table-div").html(data.html);
    $("#new_order_modal").attr("args", data.id);
    Dajaxice.purchasing.getOngoingOrderList(getOrderListCallBack,{});
}

//selectall
$(document).on("click", "input#selectall", function(){
    var target = this.checked;
    $("input[type='checkbox']").each(function(){
        this.checked = target; 
    });
});

$(document).on("click","#add_to_order",function(){
    pendingArray = Array();
    $("input[type='checkbox']:checked").each(function(){
        pendingArray.push($(this).attr("args"));
    });
});

//new puchase order delete button
$(document).on("click","#btn-delete",function(){
    var id = $("#new_order_modal").attr("args");
    if(confirm("是否确定删除？")){
        Dajaxice.purchasing.newOrderDelete(deleteCallBack,{"id":id,});
    }
    
});
function deleteCallBack(){
    alert("删除成功");
    Dajaxice.purchasing.getOngoingOrderList(getOrderListCallBack, {});
}



$(document).on("click","#new_bid_btn",function(){
    Dajaxice.purchasing.newBidCreate(getBidCallBack, {});
})

function getBidCallBack(data) {
    $("input#bid_id").val(data.bid_id);
    $("div.table-div").html(data.html);
    $("#bid_modal").attr("args", data.id);
    Dajaxice.purchasing.getOngoingBidList(getBidListCallBack, {});
}
function getBidListCallBack(data) {
    $(".bid-select").each(function() { 
        $(this).html(data);   
    });
}
$(document).on("click",".bid-btn-open",function(){
    if($(this).hasClass("clear")) {
        pendingArray = Array();
    }
    var id = $($(this).attr("data-source")).val(); // datatable index not bid_id
    Dajaxice.purchasing.getBidForm(getBidCallBack, {"bid_id": id, "pendingArray": pendingArray, })
});
$(document).on("click","#add_to_bid",function(){
    pendingArray = Array();
    $("input.checkbox:checked").each(function() {
        pendingArray.push($(this).attr("args"));
    });
});
$(document).on("click","#bid-btn-delete",function() {
    var id = $("#bid_modal").attr("args");
    if(confirm("是否确定删除？")) {
        Dajaxice.purchasing.newBidDelete(bidDeleteCallBack, {"id": id});
    }
});
function bidDeleteCallBack(data) {
    Dajaxice.purchasing.getOngoingBidList(getBidListCallBack, {});
}
$(document).on("click","#bid-btn-save",function() {
    var id = $("#bid_modal").attr("args");
    if(confirm("是否确认保存？")) {
        Dajaxice.purchasing.newBidSave(saveCallBack, {"id": id, "pendingArray": pendingArray, });
    }
});
$(document).on("click","#bid-btn-finish",function() {
    var id = $("#bid_modal").attr("args");
    if(confirm("是否确认完成编制？")) {
        Dajaxice.purchasing.newBidFinish(finishCallBack, {"id": id});
    }
});











