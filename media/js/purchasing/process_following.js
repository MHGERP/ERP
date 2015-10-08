$("#id_bidform").hide();
$("#id_following_date").hide();
$("#id_executor").hide();


$("#add_process_following").click(function(){
    var bid=$("#process_following_table").attr("bid");
    var process_form=$("#process_info_form").serialize(true);
    Dajaxice.purchasing.AddProcessFollowing(add_process_callback,{
        "bid":bid,
        "process_form":process_form
    });
});

function add_process_callback(data){
    alert("成功");
}
