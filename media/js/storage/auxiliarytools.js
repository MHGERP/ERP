$('#date').datetimepicker({
    format: 'yyyy-mm-dd',
    autoclose:true,
    minView:'month',
});
$('input[id$=time]').datetimepicker({
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
    $('#entry_detail_form').submit(function(e){
        e.preventDefault();
        var data=$("#entry_detail_form").serialize();
        Dajaxice.storage.Auxiliary_Tools_Entry(function(msg){
            alert(msg);
            msg_type=msg.substr(0,9);
            if(msg_type=="[SUCCESS]")
            {
                $("#confirm").attr('disabled','disabled');
                $("#confirm").hide();
                $("#confirm").after('<a type="button" href="/storage/auxiliarytools/entrylist" class="btn btn-primary">返回</a>');
            }
        },
        {
            'data':data,
        });
    });
    $("#detail_form").submit(function(e){
        e.preventDefault();
        var data=$("#detail_form").serialize();
        Dajaxice.storage.Auxiliary_Tools_Apply_Commit(function(msg){
            alert(msg);
            msg_type=msg.substr(0,9);
            if(msg_type=="[SUCCESS]")
            {
                $("#confirm").attr('disabled','disabled');
                $("#confirm").hide();
                $("#confirm").after('<a type="button" href="/storage/auxiliarytools/applylist" class="btn btn-primary">返回</a>');
            }
        },
        {
            'data':data,
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
    $("#apply_card_form").submit(function(e){
        e.preventDefault();
        var data=$("#apply_card_form").serialize();
        Dajaxice.storage.Search_Auxiliary_Tools_Apply_Card(function(data){
            $('#apply_card_table').html(data);
            $('#create_time').val('');
            $('#apply_item').val('');
            $('#applicant').val('');
            $('#index').val('');
        },
        {
            'data':data,
        });
    });  
});
function SetValue(obj,model,measurement_unit,unit_price)
{
    model=model||'未选择';
    measurement_unit=measurement_unit||'未选择';
    unit_price=unit_price||'未选择';
    var target=obj.parent().parent();
    target.children('td:nth-child(3)').html(model);
    target.children('td:nth-child(4)').html(measurement_unit);
    target.children('td:nth-child(6)').html(unit_price);
    var unit_price=parseInt(unit_price);
    var value=target.children('td:nth-child(5)').children('input').val();
    target.children('td:nth-child(7)').html(value*unit_price);
}

$('select').change(function(){
    var obj=$(this);
    var id=obj.val();
    if(id)
    {
        Dajaxice.storage.Auxiliary_Detail_Query(function(data){
            SetValue(obj,data['model'],data['measurement_unit'],data['unit_price']);
        },
        {
            'id':id,
        });
    }
    SetValue(obj);
})

$('input[type=text]').keyup(function(){
    var obj=$(this);
    var value=obj.val();
    var unit_price=parseInt(obj.parent().next().html());
    obj.parent().next().next().html(value*unit_price);
})
