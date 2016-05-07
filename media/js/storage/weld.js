var mid;
var rid;
$(document).ready(function(){
    cal_entry_items_price();
    $(document).on("click","span[name='weldentry']",function(){
        var role = $(this).attr("role");
        var eid = $("#items_table").attr("eid");
        if(confirm("请确认所有内容已经填写完毕，签字后不能进行修改")){
            Dajaxice.storage.entryConfirm(entry_confirm_callback,{"role":role,"eid":eid});
        }
    })
    $(document).on("dblclick","tr[name='entry_item']",function(){
        mid = $(this).attr("id");
        change_item(this);
        $("#myModal").modal('show');
    })
    $(document).on("click","#search-btn",function(){
        Dajaxice.storage.searchWeldEntry(weld_search_callback,{"searchform":$("#search_form").serialize()});
    })
    $(document).on("click","#refund_search_btn",function(){
        var search_form = $("#refund_search_form").serialize();
        Dajaxice.storage.searchWeldRefund(weld_refund_search_callback,{"search_form":search_form});
    })
    $(document).on("dblclick","table#refund_confirm_table",function(){
        var refund_weight = $("#refund_weight").text();
        var refund_status = $("#refund_status").text();
        $("#id_refund_weight").val(refund_weight);
        $("#id_refund_status").val(refund_status);
        $("#myModal").modal('show');
    })
    $(document).on("click","#refund_confirm_save",function(){
        rid = $("div#refund_confirm_main").attr("rid");
        Dajaxice.storage.refundKeeperModify(refundkeepermodify_callback,{"form":$("form#refund_form").serialize(),"rid":rid});
    })
    $(document).on("click","span[name='weld_refund_confirm']",function(){
        rid = $("div#refund_confirm_main").attr("rid");
        var role = $(this).attr('role');
        Dajaxice.storage.weldRefundConfirm(weldrefundconfirm_callback,{"rid":rid,"role":role})
    })
        
        
})
function entry_confirm(eid){
    
}
function change_item(tr){
    var a = $(tr).find("td");
    $("input#id_remark").val(a.eq(11).children("p").eq(0).text());
        var production_date = a.eq(9).children("p").eq(0).text().replace(/\./g,'-')
    $("input#id_production_date").val(production_date);
    var price = parseFloat(a.eq(12).text());
    if(!isNaN(price))
        $("input#id_price").val(price);
}
function save_item(){
    Dajaxice.storage.entryItemSave(save_item_callback,{"form":$("#entry_item_form").serialize(),"mid":mid});
}

function save_item_callback(data){
    if(data.flag){
        $("#items_table").html(data.html);
        cal_entry_items_price();
        alert(data.message);
    }
    else{
        alert(data.message);
    }
}

function cal_entry_items_price(){
    items = $("table#items_table").find("tr[name = 'entry_item']");
    var entry_total_price = 0.0
    for( i = 0 ; i < items.length ; i++ )
    {   
        var a = $(items[i]).find("td");
        
        var price = parseFloat(a.eq(12).text());
        if(isNaN(price))
            continue;
        var count = parseFloat(a.eq(6).text());
        var total_price = price * count;
        entry_total_price += total_price;
        var op = a.eq(13).find("p");
        op.eq(0).html(total_price);
    }
    $("#entry_total_price").html(entry_total_price);
}

function entryconfirm(eid){
    var entry_code = $("#input_entry_code").val();
    Dajaxice.storage.entryConfirm(entry_confirm_callback,{"eid":eid,"entry_code":entry_code}); 
}

function entry_confirm_callback(data){
    alert(data.message);
    $("#items_table").html(data.html)
    if(role == "keeper")
        cal_entry_items_price()
}

function get_overtime(){
    Dajaxice.storage.getOverTimeItems(get_overtime_callback)
}

function get_overtime_callback(data){
   $("#item_table").html(data.html); 
}

function get_thread(){
    Dajaxice.storage.getThreadItems(get_thread_callback);
}

function get_thread_callback(data){
   $("#item_table").html(data.html); 
}
 

function humi_change_save(hid){
    Dajaxice.storage.humiChangeSave(humi_change_save_callback,{"hidform":$("#humiture_form").serialize(),"hid":hid});
}

function humi_change_save_callback(data){
    alert(data.message)
}

function bake_save(bid){
    Dajaxice.storage.bakeSave(bake_save_callback,{"bakeform":$("#weldbake_form").serialize(),"bid":bid});
}

function bake_save_callback(data){
    $("#bake_div").html(data.html);
    alert(data.message);
}

function weld_entry_search_callback(data){
   $("#search_table").html(data.html); 
}

function weld_refund_search_callback(data){
    $("div#refund_history_table").html(data.html);
}

function refundkeepermodify_callback(data){
    alert(data.message);
    if(data.flag){
        $("div#refund_confirm_main").html(data.html);
        $("#myModal").modal('hide');
    }
}

function weldrefundconfirm_callback(data){
    $("div#refund_confirm_main").html(data.html);
    alert(data.message);
}
