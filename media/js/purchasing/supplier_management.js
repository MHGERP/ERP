var mod;
$("#add_new_supplier").click(function(){
    $("#id_supplier_id").val('');
    $("#id_supplier_name").val('');
    mod=-1;
});
$(document).on("click","#upload_supplier",function(){
    var supplier_id=$(this).closest("tr").attr("id");
    mod=supplier_id;
    Dajaxice.purchasing.SupplierUpdate(supplier_update_callback,{
        "supplier_id":supplier_id
    });
    $("#id_supplier_input").val(supplier_id);
});

$(document).on("click","#edit_supplier",function(){
    var tr=$(this).closest("tr");
    mod=tr.attr("id");
    $("#id_supplier_id").val($(tr).children("td:eq(0)").html());
    $("#id_supplier_name").val($(tr).children("td:eq(1)").html());
});


$(document).on("click","#file_delete",function(){
    Dajaxice.purchasing.FileDelete(supplier_update_callback,{
        "mod":mod,
        "file_id":$(this).closest("tr").attr("id")
    });
});

$(document).on("click","#delete_supplier",function(){
    Dajaxice.purchasing.SupplierDelete(supplier_delete_callback,{
        "supplier_id":$(this).closest("tr").attr("id")
    });
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
    alert(data.message);
    $("#supplier_table").html(data.table);
}
function supplier_delete_callback(data){
    alert("删除成功！");
    window.location.reload();
}
