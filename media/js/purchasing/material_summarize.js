$(document).ready(function(){
	refresh();
})
$("#id_inventory_type").change(function(){
	refresh();
});

function refresh(){
	val = $("#id_inventory_type").val();
	Dajaxice.purchasing.chooseInventorytype(choose_Inventorytype_callback,{
		"pid":val
	});
}
function choose_Inventorytype_callback(data){
    val = $("#id_inventory_type").val();
    alert(val);
    if(val==1){
    	$("#new_purchasing_order").html(data.new_order_form_html);
    	$("#inventory_detail_table").html(data.main_material_quota_html);
    }
    else if(val==2){
    	$("#new_purchasing_order").html(data.new_order_form_html);
    	$("#inventory_detail_table").html(data.accessory_quota_html);
    }
    else if(val==3){
        $("#new_purchasing_order").html(data.new_order_form_html);
    	$("#inventory_detail_table").html(data.first_send_detail_html);
    }
    else if(val==4){
        $("#new_purchasing_order").html(data.new_order_form_html);
    	$("#inventory_detail_table").html(data.out_purchasing_detail_html);
    }
    else{
    	$("#new_purchasing_order").html(data.new_purchasing_form_html);
    	$("#inventory_detail_table").html(data.cast_detail_html);
    }
}