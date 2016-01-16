$(document).ready(refresh);

function refresh() {
    var iid = $("#div_card").attr("iid");
    Dajaxice.techdata.getTransferCard(refreshCallBack, {"iid": iid});
}
function refreshCallBack(data) {
    $("#div_card").html(data);
}

new AutoSave(".word_textarea", Dajaxice.techdata.saveProcessRequirement).init();
