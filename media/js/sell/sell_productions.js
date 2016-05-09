$(document).ready(refresh);

function refresh() {
    Dajaxice.sell.getProductionList(
        function(data){
            $("#widget-box").html(data);
        },
        {

        }
    );
}
