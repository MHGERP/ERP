$(document).ready(refresh);
$("#order_search").click(refresh);
function refresh(){
    var id_work_order = $("#id_work_order").val();
    Dajaxice.techdata.getProcessBOM(refreshCallBack, {"id_work_order": id_work_order, });
}
function refreshCallBack(data) {
    $("#widget-box").html(data);
}


$(document).on("click", ".tr_materiel", function() {
    var iid = $(this).attr("iid");
    Dajaxice.techdata.getMaterielInfo(getInfoCallBack, {"iid": iid})
});
function getInfoCallBack(data) {
    $("#base-info-area").html(data);
}
