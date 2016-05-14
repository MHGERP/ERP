var pendingArray = Array();
var dic_type = new Array();
dic_type["main_materiel"] = 1;
dic_type["auxiliary_materiel"] = 2;
dic_type["first_feeding"] = 3;
dic_type["out_purchased"] = 4;
dic_type["cooperant"] = 5;
dic_type["weld_material"] = 6;

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

    if(dic_type[val]<=2){
        $("#add_to_execute").show();
    }
    else{
        $("#add_to_execute").hide();
    }
    item = $("#new_purchasing_order");
    $("#inventory_detail_table").html(data.inventory_detail_html);
    // if(dic_type[val]==5){
    //     item.html(data.new_purchasing_form_html);
    //     $("#add_to_bid").show();
    //     $("#add_to_order").hide();
    //     Dajaxice.purchasing.getOngoingBidList(getBidListCallBack, {});
    // }
    // else{
        item.html(data.new_order_form_html);
        $("#add_to_order").show();
        $("#add_to_bid").hide();
        Dajaxice.purchasing.getOngoingOrderList(getOrderListCallBack,{"order_type":dic_type[val]});
    // }
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
$("#btn-save").click(function(){
    var id = $("#new_order_modal").attr("args");
    if(confirm("是否确认保存？")) {
        Dajaxice.purchasing.newOrderSave(saveCallBack, {"id": id, "pendingArray": pendingArray, });
        return true;
    }
    return false;
});
function saveCallBack() {
    refresh();
}

//new puchase order finish button
$("#btn-finish").click(function(){
    var id = $("#new_order_modal").attr("args");
    if(confirm("是否确认完成编制？")){
        Dajaxice.purchasing.newOrderFinish(finishCallBack,{"id":id});
        return true;
    }
    return false;
});
function finishCallBack() {
    refresh();
}

//open button
$(document).on("click",".btn-open",function(){
    if($(this).hasClass("clear")) {
        pendingArray = Array();
    }
    var id = $($(this).attr("data-source")).val();
    Dajaxice.purchasing.getOrderForm(getOrderCallBack,{"order_id":id,"pendingArray":pendingArray,});
});

//new purchase button
$(document).on("click","#new_purchase_btn",function(){
    Dajaxice.purchasing.newOrderCreate(getOrderCallBack, {"select_type":dic_type[$("#id_inventory_type").val()]});
});

function getOrderCallBack(data){
    if(data.status==1){
        alert("没有所选订购单");
        return false;
    }
    $("input#order_number").val(data.order_id);
    $("div.table-div").html(data.html);
    $("#new_order_modal").attr("args", data.id);
    Dajaxice.purchasing.getOngoingOrderList(getOrderListCallBack,{"order_type":dic_type[$("#id_inventory_type").val()]});
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
    $("input.checkbox").each(function(){
        if(this.checked) pendingArray.push($(this).attr("args"));
    });
});

//new puchase order delete button
$("#btn-delete").click(function(){
    var id = $("#new_order_modal").attr("args");
    if(confirm("是否确定删除？")){
        Dajaxice.purchasing.newOrderDelete(deleteCallBack,{"id":id,});
        return true;
    }
    return false;

});
function deleteCallBack(){
    Dajaxice.purchasing.getOngoingOrderList(getOrderListCallBack,{"order_type":dic_type[$("#id_inventory_type").val()]});
}



$(document).on("click","#new_bid_btn",function(){
    pendingArray.clear();
    Dajaxice.purchasing.newBidCreate(getBidCallBack, {});
});

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
    $("input.checkbox").each(function() {
        if(this.checked) pendingArray.push($(this).attr("args"));
    });
});
$("#bid-btn-delete").click(function() {
    var id = $("#bid_modal").attr("args");
    if(confirm("是否确定删除？")) {
        Dajaxice.purchasing.newBidDelete(bidDeleteCallBack, {"id": id});
        return true;
    }
    return false;
});
function bidDeleteCallBack(data) {
    Dajaxice.purchasing.getOngoingBidList(getBidListCallBack, {});
}
$("#bid-btn-save").click(function() {
    var id = $("#bid_modal").attr("args");
    if(confirm("是否确认保存？")) {
        Dajaxice.purchasing.newBidSave(saveCallBack, {"id": id, "pendingArray": pendingArray, });
        return true;
    }
    return false;
});
$("#bid-btn-finish").click(function() {
    var id = $("#bid_modal").attr("args");
    if(confirm("是否确认完成编制？")) {
        Dajaxice.purchasing.newBidFinish(finishCallBack, {"id": id});
        return true;
    }
    return false;
});

$("#add_to_execute").click(function(){
    if(confirm("是否确认添加至材料执行?")){
    var selectedArray = Array();
    $("input.checkbox").each(function(){
        if(this.checked) selectedArray.push($(this).attr("args"));
    });

    Dajaxice.purchasing.AddToMaterialExecute(add_to_material_execute_callback,{
        "selected":selectedArray
    });

    }
});
function add_to_material_execute_callback(data){
    if(data.message!='')alert(data.message);
    else refresh();
}


$(document).on("click", ".btn-primary", function() {
    mid = $(this).closest("tr").attr("iid");
    val = $("#id_inventory_type").val();
    key = $("#search_key").val();
    Dajaxice.purchasing.getRelatedModel(function (data) {
      $("#related_html").html(data);
      Dajaxice.purchasing.defaultRelated(function (data) {
        $("#related_table").html(data);
      }, {"index" : val, "mid" : mid});
    }, {"index" : val});
});

$(document).on("click", "#related_search", function() {
    val = $("#id_inventory_type").val();
    ch = dic_type[val];
    if (ch <= 2) {
      f1 = $("#id_mingcheng").val();
      f2 = $("#id_guige").val();
      f3 = $("#id_caizhi").val();
      //alert(f1+" "+f2+" "+f3);
      Dajaxice.purchasing.getRelatedTable(function(data) {
          $("#related_table").html(data);
      }, {"index" : val, "f1" : f1, "f2" : f2, "f3" : f3});
    }
    else if (ch == 4) {
      f1 = $("#id_mingcheng").val();
      f2 = $("#id_caizhi").val();
      //alert(f2);
      Dajaxice.purchasing.getRelatedTable(function(data) {
          $("#related_table").html(data);
      }, {"index" : val, "f1" : f1, "f2" : f2, "f3" : ""});
    }
    else if (ch == 6) {
      f1 = $("#id_mingcheng").val();
      f2 = $("#id_paihao").val();
      f3 = $("#id_guige").val();
      //alert(f1+" "+f2+" "+f3);
      Dajaxice.purchasing.getRelatedTable(function(data) {
          $("#related_table").html(data);
      }, {"index" : val, "f1" : f1, "f2" : f2, "f3" : f3});
    }
});
