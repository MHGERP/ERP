function entry_query(){
	var entry_select = $("#entry_select").val(); 
	Dajaxice.purchasing.entryConfirmQuery(entry_query_CallBack,{'entry_select':entry_select});
}
function entry_query_CallBack(data){
	$("#entry_table").html(data.html);
}

function purchasing_entry_confirm(eid,entry_typeid){
/*	alert(eid);
	alert(entry_typeid);*/
	Dajaxice.purchasing.entryInspectionConfirm(entry_inspection_confirm_callback,{"eid":eid,"entry_typeid":entry_typeid}); 
}
function entry_inspection_confirm_callback(data){
    if(data.flag){
        alert("入库单确认成功");
        window.location.reload();
    }
    else{
        alert("入库单确认失败");
    }
}
var mid,entrytype;
$(document).on("dblclick","tr[name='entry_item_tr']",function(){
    mid = $(this).attr("id");
    entrytype=$("#entrybody").attr("entrytype");
    Dajaxice.purchasing.getEntryFormInfo(function(data){
    $("#myModal").modal('show');
    $("#entry_item_form").html(data.html);

    
    $("#id_production_date").datetimepicker({
        format:'yyyy-mm-dd',
        weekStart:1,
        todayBtn: 1,
        autoclose: 1,
        todayHighlight:1,
        startView:2,
        forceParse:0,
        minView:2
    });
    },{"mid":mid,"entrytype":entrytype});
                                
});

$("#save_entry_item").click(function(){
    form=$("#entry_item_form").serialize(true);
    Dajaxice.purchasing.saveEntryItem(function(data){
        alert(data.message);
        if(data.status==0){
            window.location.reload();
        }
    },{
        "form":form,
        "mid":mid,
        "entrytype":entrytype

    });
});

$("span[role='purchaser']").click(function(){
    entrytype=$("#entrybody").attr("entrytype");
    eid=$("#entrybody").attr("entryid");
    Dajaxice.purchasing.entryPurchaserConfirm(function(data){
        window.location.reload();
    },{
        "eid":eid,
        "entrytype":entrytype
    });
});
