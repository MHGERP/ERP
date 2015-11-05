function news_form_submit(){
  var news_content = $("<input>").attr("type", "text").attr("name", "news_content").val($("#editor").html());
  $('#news_form').append($(news_content));
}
$(function (){
  $("#news_form").submit(news_form_submit);
});


$('[rel="news_delete"]').click(function(){
  var bln = window.confirm("是否确认删除该条新闻?");
  if(bln){
    var uid = $(this).attr("uid");
    Dajaxice.adminStaff.get_news_list(news_delete_callback,
                                         {'uid':uid});
  }
});
function check_news_is_void(){
  if($('#news_title').val()=='' || $('#id_news_date').val()==''){
    $('#news_release_button').attr('disabled', 'disabled');
  } else {
    $('#news_release_button').removeAttr('disabled', 'disabled');
  };
}
$('#news_title').focus(check_news_is_void);
$('#id_news_date').focus(check_news_is_void);
$('#news_title').focusout(check_news_is_void);
$('#id_news_date').focusout(check_news_is_void);
$('#news_title').keydown(check_news_is_void);
$('#id_news_date').keydown(check_news_is_void);
$('#news_title').keyup(check_news_is_void);
$('#id_news_date').keyup(check_news_is_void);
$('#news_title').change(check_news_is_void);
$('#id_news_date').change(check_news_is_void);


function news_delete_callback(data){
  if(data.is_deleted == true){
      var uid = "tr[id=" + data.uid +"]";
      console.log("successs!");
      console.log(data.message);
      console.log(uid);
      $(uid).remove();
    }
  else{
      console.log("Failed!");
      console.log(data.message);
      $("div#delete-error-panel").show();
      $("p#delete-message").text(data.message);
  }
}
