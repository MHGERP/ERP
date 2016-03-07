$(document).ready(refresh);

function refresh() {
    Dajaxice.techdata.getInstallWeldList(function(data) {
        $(".widget-content").html(data);
    }, {})
}
