$("#approve_confirm").click(function(){
    var value=$("#id_judgeresult").val();
    if(value==-1){
        alert("请选择审核结果!");
        return false;
    }
    Dajaxice.purchasing.BidformApprove(bidform_approve_callback,{
        "bid":$("#approve_form").attr("bid"),
        "value":value,
        "comment":$("#id_reason").val()
    });
});
function bidform_approve_callback(data){
    if(data.status==-1){
        alert("状态更改有误!");
    }
    else{
        if(data.status==0){
            alert("审核通过！");
        }
        else{
            alert("审核不通过，标单已经停止！");
        }
window.location.href="/purchasing/bidformapprove" ;
    }
}
