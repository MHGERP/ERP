$(document).ready(function(){
    cal_entry_items_price();
})
function entry_confirm(eid){
    
}
var mid;
function change_item(itemid){
    mid = itemid;
    var a = $("tr#"+mid).find("td");
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
    for( i = 0 ; i < items.length ; i++ )
    {   
        var a = $(items[i]).find("td");
        
        var price = parseFloat(a.eq(12).text());
        if(isNaN(price))
            continue;
        var count = parseFloat(a.eq(6).text());
        var total_price = price * count;
        var op = a.eq(13).find("p");
        op.eq(0).html(total_price);
    }
}

function entryconfirm(eid){
    var entry_code = $("#input_entry_code").val();
    Dajaxice.storage.entryConfirm(entry_confirm_callback,{"eid":eid,"entry_code":entry_code}); 
}

function entry_confirm_callback(data){
    if(data.flag){
        alert("入库单确认成功");
        window.location.reload();
    }
    else{
        alert("入库单确认失败");
    }
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
