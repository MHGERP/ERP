$(document).ready(function(){
    var aid;
    $(document).on("dblclick", "tr[name='entry_item_tr']", function(){
        aid = $(this).attr("id");
        var remark = $(this).find("td").eq(5).children("p").eq(0).text();
        $("#myModal").modal('show');
        $("#id_remark").val(remark);
    });
    $(document).on("click", "#saveItem", function(){
        var remark = $("#id_remark").val();
        Dajaxice.storage.auEntryUpdate(updateCallback, {"aid":aid, "remark":remark});
    });
    $(document).on("click", "span[name='autool']", function(){
        var role = $(this).attr("role");
        var eid = $("#items_table").attr("eid");
        if(confirm("请确认所有内容已经填写完毕，签字后不能修改！")){
            Dajaxice.storage.auToolEntryConfirm(entryConfirmCallback, {"role":role, "eid":eid});
        }
    });
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
    $(document).on("click","#auxiliarytools_search_submit",function(){
        var form=$("#apply_card_form").serialize();
        Dajaxice.storage.Search_Auxiliary_Tools_Apply_Card(function(data){
            $('#apply_card_table').html(data.html);
        },
        {
            'form':form,
        });
    })    
    $(document).on("click", "span[name='autool_apply']", function(){
        var role = $(this).attr("role");
        var aid = $(this).attr("aid");
        if(confirm("请确认所有内容已经填写完毕，签字后不能修改！")){
            Dajaxice.storage.auToolApplyCardConfirm(applycardConfirm_callback, {"role":role, "aid":aid});
        }
    });
    $(document).on("click","#au_entry_search_btn",function(){
        Dajaxice.storage.getAuxiliaryEntrySearch(function(data){
            $("#entry_table").html(data.html);
        },{
            "form":$("#au_entry_search_form").serialize(),
        });
    })
});
function auxiliarytoolapply_callback(data){
    $("#apply_form").html(data.form_html);
    $("#applycard").html(data.card_html);
    alert(data.message);
}
function applycardConfirm_callback(data){
    $("#applycard").html(data.card_html);
    alert(data.message);
}

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


function updateCallback(data){
    var aid = data.aid;
    $("tr[id="+aid+"]").find("td").eq(5).children("p").eq(0).text(data.remark);
    alert(data.message);
}

function entryConfirmCallback(data){
    $("#auxiliarytools_entry").html(data.html);
    alert(data.message);
}
