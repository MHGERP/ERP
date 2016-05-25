$("#id_bid_date").datetimepicker({
    format:'yyyy-mm-dd',
    weekStart:1,
    todayBtn: 1,
    autoclose: 1,
    todayHighlight:1,
    startView:2,
    forceParse:0,
    minView:2
});
$("#id_bid_delivery_date").datetimepicker({
    format:'yyyy-mm-dd',
    weekStart:1,
    todayBtn: 1,
    autoclose: 1,
    todayHighlight:1,
    startView:2,
    forceParse:0,
    minView:2
});
$("#id_bid_datetime").datetimepicker({
    format:'yyyy-mm-dd',
    weekStart:1,
    todayBtn: 1,
    autoclose: 1,
    todayHighlight:1,
    startView:2,
    forceParse:0,
    minView:2
});
$("#apply_confirm").click(function(){
      var form = $(this).parents("form");
      var bidapplyform = form;
      var bid_apply_id=$("#bid_apply_div").attr("bidapplyid");
      supplier_form_set=Array();
      supplier_id_set=Array();
    $(".supplierform").each(function(){
        supplier_form_set.push($(this).serialize(true));
        supplier_id_set.push($(this).attr("supplierselect"));
    });
      Dajaxice.purchasing.saveBidApply(function(data){
        if(data.status ==0 ){
            window.location.reload();
        }
        else{
            alert("表单填写有误");
        }
      },{
        'form':$(form).serialize(true),
        'bid_apply_id':bid_apply_id,
        'supplier_form_set':supplier_form_set,
        'supplier_id_set':supplier_id_set
      });

});

$("#apply_submit").click(function(){
      var bid_apply_id=$("#bid_apply_div").attr("bidapplyid");
      Dajaxice.purchasing.submitBidApply(function(data){
    window.location.reload();
      },{bid_apply_id:bid_apply_id});

});

$("#apply_comment_confirm").click(function(){
    var bid_apply_id=$("#bid_apply_div").attr("bidapplyid");
    var usertitle=$("#comment_add").attr("usertitle");
    Dajaxice.purchasing.BidApplyComment(function(data){
        window.location.reload();
    },{
        "bid_apply_id":bid_apply_id,
        "usertitle":usertitle,
        "comment":$("#comment_area").val()
    });
});
$("#apply_logistical_confirm").click(function(){
    Dajaxice.purchasing.BidApplyLogistical(function(data){
    if(data.status==0)window.location.reload();
    else alert("表单填写有误！");
    },{
    "form":$("#logistical_form").serialize(true),
    "bid_apply_id":$("#bid_apply_div").attr("bidapplyid"),
    "usertitle":$("#comment_add").attr("usertitle") 
});
});
