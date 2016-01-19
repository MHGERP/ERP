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
});
