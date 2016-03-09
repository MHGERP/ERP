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