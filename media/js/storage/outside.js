function outsideentryconfirm(eid){
    Dajaxice.storage.outsideEntryConfirm(outside_entryconfirm_callback,{"eid":eid,"form":$("#entryform").serialize(),});
}
function outside_entryconfirm_callback(data){
    $("#entrybody").html(data.html);
    alert(data.message)
} 
