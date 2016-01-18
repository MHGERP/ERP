function outsideentryconfirm(eid){
    Dajaxice.storage.outsideEntryConfirm(outside_entryconfirm_callback,{"eid":eid,"form":$("#entryform").serialize(),});
}
function outside_entryconfirm_callback(data){
    $("#entrybody").html(data.html);
    alert(data.message)
}

var applyitemid;
function change_applycard_remark(id){
    applyitemid = id;
    var remark = $("#"+applyitemid+"remark").text();
    $("input#remark_input").val(remark); 
}

function save_remark(){
    var remark = $("input#remark_input").val(); 
    Dajaxice.storage.outsideApplyCardItemRemarkChange(save_remark_callback,{"itemid":applyitemid,"remark":remark})
}

function save_remark_callback(data){
    $("#"+data.id+"remark").text(data.remark);
}

function outsideapplycardconfirm(aid){
    Dajaxice.storage.outsideApplyCardConfirm(outsideapplycardconfirm_callback,{"form":$("#applycardform").serialize(),"aid":aid});
}

function outsideapplycardconfirm_callback(data){
    $("div#applycardbody").html(data.html);
    alert(data.message);
}

function get_outsidethread(){
    Dajaxice.storage.getOutsideThreadItems(get_outsidethrea_callback);
}

function get_outsidethrea_callback(data){
    $("#item_table").html(data.html);
}
