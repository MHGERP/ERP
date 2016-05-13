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

    function getUrlParam(name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
        var r = window.location.search.substr(1).match(reg);  //匹配目标参数
        if (r != null) 
            return unescape(r[2]); 
        return null; //返回参数值
                                                    
    }
    
    $("#save_select_item").click(function(){
        var val = $("input:radio[name='item']:checked").val();
        if(val==null){
            alert("请选择一个库存材料");
        }
        else{
        $('#id_workorder').attr('disabled',false);
        Dajaxice.storage.weldMaterialApply(function(data){
           $('#id_workorder').attr('disabled',true); 
           alert(data.message)
            if(data.flag){
                $("#confirm").attr('disabled','disabled');
                $("#confirm").hide();
                $("#confirm").after('<a type="button" href="/storage/weldapply" class="btn btn-primary">返回</a>');
            }
        },
        {'itemid':val,'form':$("#detail_form").serialize(),"index":getUrlParam('index')}
    );
    }
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
    $(document).on("dblclick","table#apply_table",function(){
        aid = $(this).attr("aid");
        $("#id_actual_weight").val($("#actual_weight").text());
        $("#id_actual_quantity").val($("#actual_quantity").text());
        $("#id_remark").val($("#apply_card_remark").text());
        $("#myModal").modal('show');
    })
    $(document).on("click","#apply_item_save",function(){
        var select_item = $("input[type='radio']:checked").val();
        if($("input[name='actual_weight']").val()==""){
            $("#id_actual_weight").css("background-color","red");
            alert("请输入实发重量");
            return;
        }
        if(select_item != null){
            aid = $("table#apply_table").attr("aid");
            Dajaxice.storage.weldMaterialApply(weldapply_callback,{"apply_form":$("#apply_form").serialize(),"select_item":select_item,"aid":aid});
        }
        else{
            alert("请选择领用材料")
        }
    })
    $(document).on("click","#search_material_btn",function(){
        Dajaxice.storage.searchMaterial(search_material_callback,{"search_form":$("#search_material_form").serialize(),"search_type":"weld",});
    })
    $(document).on("click","span[name='weldapply']",function(){
        var role = $(this).attr("role");
        aid = $("table#apply_table").attr("aid");
        if(confirm("确认后不能再次修改")){
            Dajaxice.storage.weldApplyConfirm(weldapplyconfirm_callback,{"role":role,"aid":aid});
        }
    })
});
function weldapply_callback(data){
    if(data.flag){
        $("#word_contain").html(data.html);
        $("#myModal").modal("hide");
    }
    alert(data.message);
}

function search_material_callback(data){
   $("#store_items_table").html(data.html); 
}

function weldapplyconfirm_callback(data){
    $("#word_contain").html(data.html);
    alert(data.message);
}
