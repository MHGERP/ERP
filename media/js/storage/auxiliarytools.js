$('#date').datetimepicker({
    format: 'yyyy-mm-dd',
    autoclose:true,
    minView:'month',
});

$(document).ready(function(){
  $("#inventory_form").submit(function(e){
    e.preventDefault();
    var data=$("#inventory_form").serialize();
    Dajaxice.storage.Search_Auxiliary_Tools_Records(function(data){
        $('#inventory_table').html(data);
        $('#date').val('');
    },
    {
        'data':data,
        'search_type':'inventory',
    });
  });
  $("#entry_form").submit(function(e){
    e.preventDefault();
    var data=$("#entry_form").serialize();
    Dajaxice.storage.Search_Auxiliary_Tools_Records(function(data){
        $('#entry_table').html(data);
        $('#date').val('');
    },
    {
        'data':data,
        'search_type':'entry',
    });
  });
  $("#apply_form").submit(function(e){
    e.preventDefault();
    var data=$("#apply_form").serialize();
    Dajaxice.storage.Search_Auxiliary_Tools_Records(function(data){
        $('#apply_table').html(data);
        $('#date').val('');
    },
    {
        'data':data,
        'search_type':'apply',
    });
  });
});
