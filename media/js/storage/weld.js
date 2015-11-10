function entry_confirm(eid){
    
}

var mid;
function change_item(itemid){
    mid = itemid;
    var a = $("tr#"+mid).find("td");
    $("input#id_remark").val(a.eq(8).text());
    $("input#id_date").val(a.eq(9).text());
    $("input#id_price").val(a.eq(10).text());

}

function save_item(){
    Dajaxice.storage.entryItemSave(save_item_callback,{"form":$("#entry_item_form").serialize(),"mid":mid});
}

function save_item_callback(data){
    if(data.flag){
        $("div#items_table").html(data.html);
        alert(data.message);
    }
    else{
        alert(data.message);
    }
    
}
