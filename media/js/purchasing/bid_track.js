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

  $('#bid_apply_form #apply_reset').each(function(){
    $(this).click(function(){
      form = $(this).parents("form");
      Dajaxice.purchasing.resetBidApply(saveComment_callback,{'bid_id':bid_id});
    })
  })

  $('#bid_apply_form #apply_submit').each(function(){
    $(this).click(function(){
      Dajaxice.purchasing.submitStatus(saveComment_callback,{'bid_id':bid_id});
    })
  })

})
function saveComment_callback(data){
  if (data.status == "1"){
    alert(data.message);
    location.reload();
  }else if(data.status == "2"){
    alert(data.message);
  }else{
    $.each(data.field,function(i,item){
       object = $(dispatch_form).find('#'+item);
       object.css("background","white");
    });
    //error field background turn into red
    $.each(data.error_id,function(i,item){
       object = $(dispatch_form).find('#'+item);
       object.css("background","red");
    });

    alert(data.message);
  }

}
