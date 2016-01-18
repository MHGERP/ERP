$('#date').datetimepicker({
    format: 'yyyy-mm-dd',
    autoclose:true,
    minView:'month',
});
$(document).ready(function(){
  $("#query_form").submit(function(e){
    e.preventDefault();
    var data=$("#query_form").serialize();
    Dajaxice.storage.Search_History_Apply_Records(function(data){
        $('#history_table').html(data);
        $('#date').val('');
    },
    {
        'data':data,
    });
  });
//  if($("#status").val()==3)
// {
//     $("#confirm").attr('disabled','disabled');
//     $("#confirm").hide();
//     $("#confirm").after('<a type="button" href="/storage/weldapply" class="btn btn-primary">返回</a>');
//
// }
});
