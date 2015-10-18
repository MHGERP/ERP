$(function(){
  urls = window.location.href.split("/");
  bid_id = urls[urls.length-2]
  $('#bid_form .btn').each(function(){
    $(this).click(function(){
      form = $(this).parents("form");
      Dajaxice.purchasing.saveComment(saveComment_callback,{'form':$(form).serialize(true),'bid_id':bid_id});
    })
  })

  $('#bid_apply_form #apply_confirm').each(function(){
    $(this).click(function(){
      form = $(this).parents("form");
      Dajaxice.purchasing.saveBidApply(saveComment_callback,{'form':$(form).serialize(true),'bid_id':bid_id});
    })
  })
})
function saveComment_callback(data){
  if (data.status == "1"){
    // if success all field background turn into white
    // $(dispatch_div).html(data.table);
    //alert(data.message);
    //location.reload();
  }else{
    alert(data.message);
  }

}
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
