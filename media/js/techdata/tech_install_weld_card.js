$(document).ready(refresh);

function refresh() {
    var iid = $("#div_card").attr("iid");
    Dajaxice.techdata.getTechInstallWeldCard(function(data) {
        $("#div_card").html(data);
    }, {"iid": iid, });
}
