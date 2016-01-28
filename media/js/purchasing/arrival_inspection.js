function entry_query(){
	var entry_select = $("#entry_select").val();
	Dajaxice.purchasing.entryConfirmQuery(entry_query_CallBack,{'entry_select':entry_select});
}
function entry_query_CallBack(data){
	$("#entry_table").html(data.html);
}