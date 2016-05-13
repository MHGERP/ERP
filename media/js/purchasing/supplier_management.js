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

$(document).on("click", "#quote_supplier", function() {
    supid = $(this).closest("tr").attr('id');
    Dajaxice.purchasing.getQuotingList(function(data) {
      $("#quote_table").html(data);
    }, {"supid" : supid});
    $("#add_quoting").val(supid);
});

$(document).on("click", "#delete_quoting", function() {
    quoteid = $(this).closest("tr").attr('id');
    //alert(quoteid);
    Dajaxice.purchasing.quotingDelete(function(data) {
      $("#quote_table").html(data);
    }, {"quoteid" : quoteid});
});

$(document).on("click", "#add_quoting", function() {
    supid = $(this).val();
    quoteid = "0";
    Dajaxice.purchasing.quotingAdd(function(data) {
      //alert(data);
      $("#quote_table").html(data);
    }, {"supid" : supid, "quoteid" : quoteid});
    $("#add_quoting").attr({"style":"display:none"});
});

$(document).on("click", "#edit_quoting", function() {
    quoteid = $(this).closest("tr").attr('id');
    // alert(quoteid);
    Dajaxice.purchasing.quotingAdd(function(data) {
      //alert(data);
      $("#quote_table").html(data);
    }, {"supid" : supid, "quoteid" : quoteid});
    $("#add_quoting").attr({"style":"display:none"});
});

$(document).on("click", "#add_edit_save", function() {
    supid = $(this).val();
    quoteid = $(this).attr("name");
    f1 = $("#add_edit1").val();
    f2 = $("#add_edit2").val();
    f3 = $("#add_edit3").val();
    f4 = $("#add_edit4").val();
    f5 = $("#add_edit5").val();
    Dajaxice.purchasing.quotingSave(function(data) {
        Dajaxice.purchasing.getQuotingList(function(data) {
          $("#quote_table").html(data);
        }, {"supid" : supid});
    }, {"supid" : supid, "quoteid" : quoteid, "f1" : f1, "f2" : f2, "f3" : f3, "f4": f4, "f5" : f5});
    $("#add_quoting").removeAttr("style");
});
