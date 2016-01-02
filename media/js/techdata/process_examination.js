$(document).ready(refresh);



function refresh() {
    var id_work_order = $("#id_work_order").val();
    Dajaxice.techdata.getTechdataList(getTechdataListCallBack, {"id_work_order": id_work_order});
}
function getTechdataListCallBack(data) {
	
    $("#widget-content").html(data);
}

$("#order_search").click(function() {
	refresh();
});

function getIndexCallBack(data) {
    $("#widget-content").html(data);
}