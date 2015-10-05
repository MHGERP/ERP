var mod;
$("#add_new_supplier").click(function(){
    $("#id_supplier_id").val('');
    $("#id_supplier_name").val('');
    mod=-1;
});
$(document).on("click","#upload_supplier",function(){
    var supplier_id=$(this).closest("tr").attr("id");
    Dajaxice.purchasing.SupplierUpdate(supplier_update_callback,{
        "supplier_id":supplier_id
    });
});

$(document).on("click","#edit_supplier",function(){
    var tr=$(this).closest("tr");
    mod=tr.attr("id");
    $("#id_supplier_id").val($(tr).children("td:eq(0)").html());
    $("#id_supplier_name").val($(tr).children("td:eq(1)").html());
});

function supplier_update_callback(data){
    $("#file_table").html(data.supplier_html);
}

$("#add_or_update_supplier").click(function(){
        //$("#template_notice_error_message").empty();
    Dajaxice.purchasing.SupplierAddorChange(add_or_change_supplier_callback,{
        "mod":mod,
        "supplier_form":$("#supplier_info_form").serialize(true),
        
    });
});

function add_or_change_supplier_callback(data){
    $("#supplier_table").html(data.table);
}
