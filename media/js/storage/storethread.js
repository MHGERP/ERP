function change_storethread(itemid){
    mid = itemid;
    var a = $("tr#"+mid).find("td");
    $("input#id_specification").val(a.eq(1).text());
    $("input#id_count").val(a.eq(3).text());
}

function delete_storeThread(itemid){
    mid = itemid;
    Dajaxice.storage.storeThreadDelete(save_storeThreadEntry_callback,{"mid":mid});
}

function delete_storeThread_callback(data){
    if(data.flag){
        alert(data.message);
        $("div#items_table").html(data.html);
    }
    else{
        alert(data.message);
    }
}

function save_storeThreadEntry(){
    Dajaxice.storage.storeThreadSave(save_storeThreadEntry_callback,{"form":$("#entry_item_form1").serialize(),"mid":mid});
}

function save_storeThreadEntry_callback(data){
    if(data.flag){
        alert(data.message);
        $("div#items_table").html(data.html);
    }
    else{
        alert(data.message);
    }
}

function add_storeThread(){
    Dajaxice.storage.storeThreadAdd(add_storeThread_callback,{"form":$("#entry_item_form2").serialize()});
}

function add_storeThread_callback(data){
    if(data.flag){
        alert(data.message);
        $("div#items_table").html(data.html);
    }
    else{
        alert(data.message);
    }
}

function add_storeThreadEntry(){

    $("input#id_specification").val("");
    $("input#id_count").val("");
}
