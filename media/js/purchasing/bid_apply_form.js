
$("#apply_confirm").click(function(){
      var form = $(this).parents("form");
      var bidapplyform = form;
      var bid_apply_id=$("#bid_apply_div").attr("bidapplyid");
      Dajaxice.purchasing.saveBidApply(function(data){
    window.location.reload();
      },{'form':$(form).serialize(true),'bid_apply_id':bid_apply_id});

});

$("#apply_submit").click(function(){
      var bid_apply_id=$("#bid_apply_div").attr("bidapplyid");
      Dajaxice.purchasing.submitBidApply(function(data){
    window.location.reload();
      },{bid_apply_id:bid_apply_id});

});
