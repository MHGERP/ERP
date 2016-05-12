
$("#id_apply_date").datetimepicker({
    format:'yyyy-mm-dd',
    weekStart:1,
    todayBtn: 1,
    autoclose: 1,
    todayHighlight:1,
    startView:2,
    forceParse:0,
    minView:2
});

$("#suppliercheck_confirm").click(function(){
    var form=$("#supplier_check_form");
    var supplier_check_id=$("#supplier_check_div").attr("suppliercheckid");
    supplier_form_set=Array();
    supplier_id_set=Array();
    $(".supplierform").each(function(){
        supplier_form_set.push($(this).serialize(true));
        supplier_id_set.push($(this).attr("supplierselect"));
    });
    Dajaxice.purchasing.saveSupplierCheck(function(data){
        if(data.status ==0 ){
            window.location.reload();
        }
        else{
            alert("表单填写有误");
        }
    },{
        'form':$(form).serialize(true),
        'supplier_check_id':supplier_check_id,
        'supplier_form_set':supplier_form_set,
        'supplier_id_set':supplier_id_set
    });
});
$("#suppliercheck_submit").click(function(){
      var supplier_check_id=$("#supplier_check_div").attr("suppliercheckid");
      Dajaxice.purchasing.submitSupplierCheck(function(data){
    window.location.reload();
      },{'supplier_check_id':supplier_check_id});
});
$("#suppliercheck_comment_confirm").click(function(){
    var supplier_check_id=$("#supplier_check_div").attr("suppliercheckid");
    var usertitle=$("#comment_add").attr("usertitle");
    Dajaxice.purchasing.SupplierCheckComment(function(data){
        window.location.reload();
    },{
        "supplier_check_id":supplier_check_id,
        "usertitle":usertitle,
        "comment":$("#comment_area").val()
    });
});
