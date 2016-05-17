$("#following_search").click(function(){
    var bidid =$("#search_input").val();
    Dajaxice.purchasing.searchPurchasingFollowing(search_purchasing_callback,{
        'bidid':bidid
    });
});

function search_purchasing_callback(data){
    $("#following_table").html(data.html);
}

var btn,aid;

$("table[name='confirm']").find("button").live("click",function(){
    var cid=$(this).attr("cid");
    btn = $(this);
    aid=$(this).parents("tr").attr("aid");
    if(cid=="ins")return false;
    if(btn.attr("Class").replace(" ","") == "btn"){
    Dajaxice.purchasing.checkArrival(check_arrival_callback,{'aid':aid,'cid':cid});
    }
});
$("#check_add_confirm").click(function(){
    Dajaxice.purchasing.ArrivalCheckAdd(function(data){
        Dajaxice.purchasing.checkArrival(check_arrival_callback,{'aid':aid,'cid':'ins'});
    },{
        'aid':aid,
        'form':$("#add_form").serialize(true)
    });
});
function check_arrival_callback(data){
    if(data.isOk){
        btn.removeClass().addClass("btn btn-success");
        alert(data.message);
    }
    else
        alert(data.message);
    if(data.isForbiden){
        $("[aid="+data.aid +"]").find("input").eq(0).attr("disabled",false);
    }
}

function gen_entry(bid){
    btn = $(this);
    var box=$("#arrivalinspection_table").find(".arrival_checkbox");
    var selected=new Array();
    for(var i=0;i<box.length;++i)
    {
        if(box[i].checked){
            var val=box[i].parentNode.parentNode.getAttribute('aid');
            selected.push(val);
        }
    }
    if(selected.length==0){
        alert("没有选定入库信息!");
        return false;
    }

    Dajaxice.purchasing.genEntry(gen_entry_callback,{'selected':selected,'bid':bid,"entry_type":$("#entry_type").val()});
}

function gen_entry_callback(data){
    // if(data.flag){
    //    alert(data.message);
    //    $("#genbtn").remove();
    // }
    // else{
    //    alert(data.message);
    // }
    alert(data.message);
    window.location.reload();
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
        $("#entry_confirm").remove();
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
        alert(data.message);
    }
    else{
        alert(data.message);
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
    is_add = false;
}

function delete_item(id){
    item_id = id;
    var sid = $("#subapply").attr("sid");
    Dajaxice.purchasing.deleteItem(delete_item_callback,{"item_id":item_id,"sid":sid});
}

function delete_item_callback(data){
    if(data.flag){
        $("tr#"+item_id).remove();
        alert("删除成功");
    }
    else{
        alert("删除失败");
    }
}

function select_entry_type(bid){
    btn = $(this);
    var box=$("#arrivalinspection_table").find(".arrival_checkbox");
    var selected=new Array();
    for(var i=0;i<box.length;++i)
    {
        if(box[i].checked){
            var val=box[i].parentNode.parentNode.getAttribute('aid');
            selected.push(val);
        }
    }
    if(selected.length==0){
        alert("没有选择入库材料信息!");
        return false;
    }
    Dajaxice.purchasing.selectEntryType(select_entry_type_callback,{"bid":bid,"selected":selected,"selectentryform":$("#selectentryform").serialize()});

}


var items_set;
var selectvalue;
var bid;
function select_entry_type_callback(data){
    $("#additemstable").html(data.html);
    items_set = data.items_set;
    selectvalue = data.selectvalue;
    bid = data.bid;
    $('#myModal').modal('show');
}

function save_entry_items(){
    //Dajaxice.purchasing.genEntry(save_entry_items_callback,{"items_set":items_set,"selectvalue":selectvalue,"bid":bid});
}

function save_entry_items_callback(data){
    if(data.isOk){
        $("#arrInsTable").html(data.html);
        alert("入库单创建成功，请完善信息后确认");
    }
    else{
        alert("入库单创建失败");
    }
}
