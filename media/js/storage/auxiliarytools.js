$('#date').datetimepicker({
    format: 'yyyy-mm-dd',
    autoclose:true,
    minView:'month',
});

$(document).ready(function(){
  $("#query_form").submit(function(e){
    e.preventDefault();
    var data=$("#query_form").serialize();
    Dajaxice.storage.Search_Auxiliary_Tools_Inventory(function(data){
        $('#inventory_table').html(data);
        $('#date').val('');
    },
    {
        'data':data,
    });
  });
});
