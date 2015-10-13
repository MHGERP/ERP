function hide_extra_form(){
    $("#id_bidform").hide();
    $("#id_following_date").hide();
    $("#id_executor").hide();
}

$("#add_process_following").click(function(){
    $("#process_info_form").ajaxSubmit({
        url:"/purchasing/processfollowingadd",
        type:"POST",
        clearForm:true,
        resetForm:true,
        error:function(data){

        },
        success:function(data){
            if(data.status===0){
                alert("添加成功");
                window.location.reload();
            }
            else{
                $("#add_form").html(data.form_html);
                hide_extra_form();
            }
        }

    });
});

function add_process_callback(data){
    alert("成功");
}

$("#add").click(function(){
   hide_extra_form(); 
});

$("#processfollowing_submit").click(function(){
    Dajaxice.purchasing.ProcessFollowingSubmit(status_submit_callback,{
        "bid":$("#process_following_table").attr("bid")
    });
    
});

function status_submit_callback(data){
    if(data.status==0){
        alert("过程跟踪完成!");
        window.location.href="/purchasing/purchasingfollowing" ;
    }
    else{
        alert("状态更改有误！");
    }
}
