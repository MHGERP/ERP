$("#approve_confirm").click(function(){
    var value=$("#id_judgeresult").val();
    if(value==-1){
        alert("请选择审核结果!");
    }
});
