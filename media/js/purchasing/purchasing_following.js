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
        alert(data.message);
    }
    else{
        alert(data.message);
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
var item_id;
var is_add;
function add_item(){
    is_add = true;
    document.getElementById("item_form").reset();
}

function subitem_save(){
    var sid = $("#subapply").attr("sid");
    data = {'subform':$("#item_form").serialize(),"sid":sid}
    if(!is_add){
        data["item_id"] = item_id;
    }
    Dajaxice.purchasing.addChangeItem(subitem_save_callback,data);
}

function subitem_save_callback(data){
    if(data.flag){
        $('#subtable').html(data.html);      
        $('#myModal').modal('hide');
        location.reload();
        alert("添加成功");
    }
    else{
        alert("添加失败，有未填写的内容");
    }
}

function add_subapply(){
    Dajaxice.purchasing.addSubApply(add_subapply_callback);
}

function add_subapply_callback(data){
    window.location.href=data.url;
}

function change_item(id){
    item_id = id;
    a = $("tr#"+item_id).find("td");
    for(var i = 0 ; i < 8 ; i++){
        var did = 'div#div'+(i+1);
        var in_obj = $(did).find("input");  
        in_obj.val(a.eq(i).text());
    } 
}

function delete_item(id){
    item_id = id;
    var sid = $("#subapply").attr("sid");
    Dajaxice.purchasing.deleteItem(delete_item_callback,{"item_id":item_id,"sid":sid});
}

function delete_item_callback(data){
    if(data.flag){
        alert("删除成功");
        $("tr#"+item_id).remove();
    }
    else{
        alert("删除失败");
    }
}
