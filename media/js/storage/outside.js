var mid;
$(document).ready(function(){
    $(document).on("click","button#search_btn",function(){
        var role = $(this).attr('role');
        Dajaxice.storage.outsideCardSearch(outsidecardsearch_callback,{"role":role,"form":$("#search_form").serialize()})
    })
    $(document).on("dblclick","tr[name='entry_item_tr']",function(){
        mid = $(this).attr("id");
        Dajaxice.storage.getOutsideEntryItemFormInfo(getforminfo_callback,{"mid":mid});
        $("#myModal").modal('show');
    })
    $(document).on("click","#save_entry_item",function(){
        var form = $("#entry_item_form").serialize();
        Dajaxice.storage.outsideEntryItemSave(outsideentryitemsave_callback,{"form":form,"mid":mid});
    })
    $(document).on("click","span[name='outside_entry_confirm']",function(){
        var eid = $(this).attr("eid");
        Dajaxice.storage.outsideEntryConfirm(outsideentryconfirm_callback,{"eid":eid});
    })
});

function getforminfo_callback(data){
    $("#entry_item_form").html(data.html); 
}

function outsidecardsearch_callback(data){
    $("#card_table").html(data.html);
}

function outsideentryconfirm_callback(data){
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

function outsideentryitemsave_callback(data){
    $("#entry_item_form").html(data.html); 
    alert(data.message);
    if(data.flag) $("#myModal").modal("hide")
}
