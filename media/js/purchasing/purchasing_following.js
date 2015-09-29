$("#following_search").click(function(){
    var bidid =$("#search_input").val();
    Dajaxice.purchasing.searchPurchasingFollowing(search_purchasing_callback,{
        'bidid':bidid
    });
});

function search_purchasing_callback(data){
    $("#following_table").html(data.html);
}

var btn;

$("table[name='confirm']").find("button").bind("click",function(){
    var cid=$(this).attr("cid");
    var aid=$(this).parents("tr").attr("aid");
    btn = $(this);
    Dajaxice.purchasing.checkArrival(check_arrival_callback,{'aid':aid,'cid':cid});
})

function check_arrival_callback(data){
    if(data.flag){
       btn.removeClass().addClass("btn btn-success");
    }
    else{
        btn.removeClass().addClass("btn");
    }
}

function gen_entry(bid){
    Dajaxice.purchasing.genEntry(gen_entry_callback,{'bid':bid});
}

function gen_entry_callback(data){
    if(data.flag){
        alert("入库单生成成功");
    }
    else{
        alert("入库单生成失败，有未确认的项,请仔细检查");
    }
}
