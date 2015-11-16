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


$('select').change(function(){
    var obj=$(this);
    var id=obj.val();
    if(id)
    {
        Dajaxice.storage.Auxiliary_Detail_Query(function(data){
            obj.parent().parent().children('td:nth-child(3)').html(data['model']);
            obj.parent().parent().children('td:nth-child(4)').html(data['measurement_unit']);
            obj.parent().parent().children('td:nth-child(6)').html(data['unit_price']);
            var unit_price=parseInt(data['unit_price']);
            var value=obj.parent().parent().children('td:nth-child(5)').children('input').val();
            obj.parent().parent().children('td:nth-child(7)').html(value*unit_price);
        },
        {
            'id':id,
        });
    }
})

$('input[type=text]').keyup(function(){
    var obj=$(this);
    var value=obj.val();
    var unit_price=parseInt(obj.parent().next().html());
    obj.parent().next().next().html(value*unit_price);
})