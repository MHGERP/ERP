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

function fill(iid) {
    if(iid == -1) {

    }
    Dajaxice.sell.getProductionForm(
        function(data) {
            $("#product_form").html(data);
            $("#product_modal").modal("show");
        },
        {
            "iid" : iid,
        }
    );
}

$("#add_product").click(function(){
    fill(-1);
});
