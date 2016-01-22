$(document).on("click", "#order_search", refresh);
function refresh() {
	var s = $("#table_select").val();
    if (s == "5"){
    	var id_work_order = $("#id_work_order").val();
    	Dajaxice.techdata.getWeldSeamWeight(refreshCallBack, {"id_work_order": id_work_order, });
    }

    	
}
function refreshCallBack(data) {
		if(data.read_only) {
        $("#id_save").hide();
        $("#id_calculate").hide();
    }
    else {
        $("#id_save").show();
        $("#id_calculate").show();
    }
    $("#detail_table").html(data.html);
}