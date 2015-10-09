$(function(){
  $('#bid_form .btn').each(function(){
    $(this).click(function(){
      form = $(this).parents("form");

      Dajaxice.purchasing.saveComment(saveComment_callback,{'form':$(form).serialize(true),'bid_id':'444'});
    })
  })
})
function saveComment_callback(data){
  if (data.status == "1"){
    // if success all field background turn into white
    // $(dispatch_div).html(data.table);
  }else{
  }
  alert(data.message);
}
