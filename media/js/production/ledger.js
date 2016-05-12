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
    var date = $('#id_complete_plandate').attr("value");
    if(date == "")
    {    
        alert("计划日期不能为空！");
        return ; 
    }

    Dajaxice.production.materialPlantimeChange(plantime_change_callback,{'mid':mid,'date':date});
}

function plantime_change_callback(data){
    $('#ledger_plantime_modal').modal("hide");
    alert("修改成功");
    $('#weld_part_order_info_modal').modal("show");
    $('#tableBody').html(data.html);
}

function modal_close(){
    $('#weld_part_order_info_modal').modal("show");
}
