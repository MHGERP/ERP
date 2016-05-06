$(document).on("click","#ledgerSearchForm .btn", function(){
  Dajaxice.production.ledgerSearch(ledger_callback,{"form":$("#ledgerSearchForm").serialize(),});

})

function ledger_callback(data){
    $('#designBOM_table').html(data.html);
}

$(document).on("click","table td",function(){
    var iid = $(this).parent().attr("iid");
    Dajaxice.production.weldPartOrderInfo(weld_part_order_info_callback,{"iid":iid});
})

function weld_part_order_info_callback(data){
    $("#weld_part_order_info_modal").modal("show");
    $('#tableBody').html(data.html);
}