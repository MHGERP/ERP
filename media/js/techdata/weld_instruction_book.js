$(document).ready(refresh);

function refresh() {
    var wwi_id = $("#div_card").attr("wwi_id");
    Dajaxice.techdata.getCard(function(data){
        $("#div_card").html(data);
    },{"wwi_id":wwi_id});
}

