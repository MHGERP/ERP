$(document).ready(refresh);

function refresh() {
    var card_id = $(".widget-content").attr("card_id");
    Dajaxice.techdata.getHeatPointDetail(function(data) {
        $(".widget-content").html(data);
    }, {"card_id": card_id, });
}

