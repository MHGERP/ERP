$(document).ready(refresh);

function refresh() {
    Dajaxice.techdata.getCard(function(data){
        $("#div_card").html(data);
    },{});
}

