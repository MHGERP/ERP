$(document).ready(refresh);
$("#order_search").click(refresh);

function refresh() {
    var id_work_order = $("#id_work_order").val();
    Dajaxice.techdata.getWeldSeamList(refreshCallBack, {"id_work_order": id_work_order, });
}
function refreshCallBack(data) {
    $("#widget-content").html(data);
}
