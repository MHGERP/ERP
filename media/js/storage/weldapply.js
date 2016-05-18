var aid;
$(document).ready(function(){
  $(document).on("click","button#search_submit",function(){
    var data=$("#query_form").serialize();
    Dajaxice.storage.Search_History_Apply_Records(function(data){
        $('#history_table').html(data);
    },
    {
        'data':data,
    });
  });
    $("#confirm").click(function(){
        var specification = $("#id_standard").val();
        Dajaxice.storage.weldMaterialStorageItems(function(data){
            $("#itemlist_div").html(data.html)
        },
        {'specification':specification}
    );
    });

    $("#refund_confirm").click(function(){
        var rid = $(this).attr("rid");
        $('#receipts_time').attr('disabled',false); 
        $('#id_receipts_code').attr('disabled',false); 
        Dajaxice.storage.weldRefundCommit(weldrefundcommit_callback,{'rid':rid,'form':$("#detail_form").serialize()})
    })

    function weldrefundcommit_callback(data){
        $('#receipts_time').attr('disabled',true); 
        $('#id_receipts_code').attr('disabled',true); alert(data.message)
        if(data.is_show)
        {
            $("#refund_confirm").attr('disabled','disabled');
            $("#refund_confirm").hide();
            $("#refund_confirm").after('<a type="button" href="/storage/weldrefund" class="btn btn-info">返回</a>');
        }
    }
    $(document).on("click","span[name='weldapply']",function(){
        var role = $(this).attr("role");
        aid = $("table#apply_table").attr("aid");
        if(confirm("确认后不能再次修改")){
            Dajaxice.storage.weldApplyConfirm(weldapplyconfirm_callback,{"role":role,"aid":aid});
        }
    })
});

function weldapplyconfirm_callback(data){
    $("#word_contain").html(data.html);
    alert(data.message);
}
