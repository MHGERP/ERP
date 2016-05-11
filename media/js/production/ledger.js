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
    $("#weld_part_order_info_modal").modal({backdrop:'static',keyboard:false});
    $("#weld_part_order_info_modal").modal("show");
    $('#tableBody').html(data.html);
}

function ledger_plantime_change(){
    var mid = $('#ledger_info_table').attr("value") ;
    Dajaxice.production.ledgerTimeChange(ledger_plantime_change_callback,{'mid':mid});
}

function ledger_plantime_change_callback(data){
    $("#weld_part_order_info_modal").modal("hide");
    $("#ledger_plantime_modal").modal({backdrop:'static',keyboard:false});
    $("#ledger_plantime_modal").modal("show");
    $('#ledger_plantime_table').html(data);
    $("#id_complete_plandate").datetimepicker({
        format:'yyyy-mm-dd',
        minView: 2,
        autoclose: true,
    });
}

function plantime_change(){
    var mid = $('#ledger_info_table').attr("value");
    Dajaxice.production.material_plantime_change(plantime_change_callback,{'mid':mid});
}

function plantime_change_callback(data){

}
