
$("#id_accept_date").datetimepicker({
    format:'yyyy-mm-dd',
    weekStart:1,
    todayBtn: 1,
    autoclose: 1,
    todayHighlight:1,
    startView:2,
    forceParse:0,
    minView:2
});
/*
bidapplyform = "";
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
      bidapplyform = form;
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

  $('#contract_confirm').each(function(){
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
       object = $(bidapplyform).find('#id_'+item);
       object.css("background","white");
    });
    //error field background turn into red
    $.each(data.error_id,function(i,item){
       object = $(bidapplyform).find('#id_'+item);
       object.css("background","red");
    });

    alert(data.message);
  }

}

*/

$("#apply_select_confirm").click(function(){
   var val=$("#bid_method_select").val();
   var bidid=$("#bid_invite_buttons").attr('bidid');
   Dajaxice.purchasing.BidApplySelect(function(data){
       window.location.reload();
   },{
       'val':val,
       "bidid":bidid
   });
});

$("#apply_fill_confirm").click(function(){
   var bidid=$("#bid_invite_buttons").attr('bidid');
   Dajaxice.purchasing.BidApplyFillFinish(function(data){
       window.location.reload();
   },{
    "bidid":bidid
   });
});
$("#apply_carry_confirm").click(function(){
   var bidid=$("#bid_invite_buttons").attr('bidid');
   Dajaxice.purchasing.BidApplyCarryFinish(function(data){
       window.location.reload();
   },{
    "bidid":bidid,
    "form":$("#bid_acceptance_form").serialize(true)
   });
});
$("#bid_apply_complete").click(function(){
   var bidid=$("#bid_invite_buttons").attr('bidid');
   Dajaxice.purchasing.BidApplyFillFinish(function(data){
       window.location.reload();
   },{
    "bidid":bidid
   });
});
