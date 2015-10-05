$(document).ready(function(){
	refresh();
})
$("#id_inventory_type").change(function(){
	refresh();
});

function refresh(){
	val = $("#id_inventory_type").val();
	if(val==-1){
		location.reload(true);
	}
	else{
		Dajaxice.purchasing.chooseInventorytype(choose_Inventorytype_callback,{
			"pid":val
		});
		alert("ehllo");
	}
}
function choose_Inventorytype_callback(data){
	alert(data.inventory_detail_html);
	$("#inventory_detail_table").html(data.inventory_detail_html);
}