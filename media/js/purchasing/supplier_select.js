$(document).on("click","#select_confirm",function(){
    var box=$("#supplier_select_table").find(".supplier_checkbox");
    var selected=new Array();
    for(var i=0;i<box.length;++i)
    {
        if(box[i].checked){
            var val=box[i].parentNode.parentNode.getAttribute('id');
            selected.push(val);
        }
    }
    if(selected.length==0){
       // $("#info_alert").html("没有选定课程!");
       // $("#alert_info_modal").modal('show');
        alert("没有选定课程!");
        return false;
    }
    Dajaxice.purchasing.SelectSupplierOperation(select_supplier_callback,{
        "selected":selected,
        "bid":$("#supplier_select_table").attr("bid")
    });
});

$(document).on("click","#select_reset",function(){
    Dajaxice.purchasing.SelectSupplierReset(select_supplier_callback,{
        "bid":$("#supplier_select_table").attr("bid")
    })
});
function select_supplier_callback(data){
    alert(data.status);
    window.location.reload();

}

$("#supplier_search").click(function(){
    var sid =$("#search_input").val();
    Dajaxice.purchasing.searchSupplier(search_supplier_callback,{
        'sid':sid,
        "bid":$("#supplier_select_table").attr("bid")
    });
});

function search_supplier_callback(data){
    $("#supplier_select_table").html(data.html);
}

$("#select_submit").click(function(){
    Dajaxice.purchasing.SelectSubmit(select_submit_callback,{
        "bid":$("#supplier_select_table").attr("bid")
    });
});
function select_submit_callback(data){
    if(data.status==0){
    alert("供应商提交成功!");
     window.location.href="/purchasing/purchasingfollowing" ;
    }
    else if (data.status==1){
        alert("没有选择供应商，提交失败");
    }
    else alert("状态更改有误！")
}

$(document).on("click", "#quotingbid", function() {
    supid = $(this).closest("tr").attr("id");
    bidid = $("#supplier_select_table").attr("bid");
    //alert("供应商报价id:"+supid+" "+"标单id:"+bidid);
    Dajaxice.purchasing.selectSupplier(function(data) {
        $("#the_supplier_quoting").html(data);
    }, {"supid" : supid, "bidid" : bidid});
});
