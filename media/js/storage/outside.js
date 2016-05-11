$(document).ready(function(){
    $(document).on("click","button#search_btn",function(){
        var role = $(this).attr('role');
        Dajaxice.storage.outsideCardSearch(outsidecardsearch_callback,{"role":role,"form":$("#search_form").serialize()})
    })
});

function outsidecardsearch_callback(data){
    $("#card_table").html(data.html);
}

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

function account_entry_search(){
    Dajaxice.storage.outsideAccountEntrySearch(accounEntrySearch_callback,{"form":$("#search_form").serialize()}); 
};

function accounEntrySearch_callback(data){
    $("#entry_main").html(data.html);
}

function account_applycard_search(){
    Dajaxice.storage.outsideAccountApplyCardSearch(accounApplyCardSearch_callback,{"form":$("#search_form").serialize(),});
}

function accounApplyCardSearch_callback(data){
    $('#applycard_main').html(data.html);
}

function outside_thread_search(){
    Dajaxice.storage.outsideThreadSearch(outsideThreadSearch_callback,{"form":$("#search_form").serialize()});
}

function outsideThreadSearch_callback(data){
    $('#item_table').html(data.html);
}
