$(document).ready(refresh);

function refresh() {
    Dajaxice.techdata.getExcuteList(refreshCallBack, {});
}
function refreshCallBack(data) {
    $(".widget-content").html(data);
}
