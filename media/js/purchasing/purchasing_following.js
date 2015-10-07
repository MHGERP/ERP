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

function entry_confirm(pid){
    var e_items = new Array();
    var cnt = 0;
    var fields = {"0":"standard","1":"status","2":"remark"};
    var entry_time = $("#entry_time").val();
    var receipts_code = $("#receipts_code").val();
    var pur_entry = {"pid":pid,"receipts_code":receipts_code,"entry_time":entry_time};
    $("#items_table tbody tr").each(function(){
        var tds = $(this).find("input");
        var eid = $(this).attr("eid");
        var item = {};
        item["eid"] = eid;
        for( var i = 0 ; i < 3; i++ ){
            item[fields[i]] = tds.eq(i).val();
        }
        e_items[cnt] = item;
        cnt += 1;
    });
    Dajaxice.purchasing.entryConfirm(entry_confirm_callback,{'e_items':e_items,'pur_entry':pur_entry});
}

function entry_confirm_callback(data){
    if(data.flag){
        alert(data.message);
    }
    else{
        alert(data.message);
    }
}
