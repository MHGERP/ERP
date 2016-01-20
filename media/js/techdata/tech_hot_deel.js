$(document).ready(refresh);

function refresh() {
    Dajaxice.techdata.getHeatTreatMaterielList(function(data){
        $("#widget-content-1").html(data);
    }, 
    {});
    Dajaxice.techdata.getHeatTreatCardList(function(data){
        $("#widget-content-2").html(data);
    }, 
    {});
}

$(document).on("click", "#select_all", function() {
    var flag = this.checked;
    $("input[type='checkbox']").each(function() {
        this.checked = flag;
    });
});

$(document).on("click", "#new_card", function() {
    var selected_item = Array();
    $("input[type='checkbox']").each(function() {
        if(this.checked) {
            selected_item.push($(this).attr("args"));
        }
    }); 
    Dajaxice.techdata.createNewHeatTreatCard(refresh, {"selected_item": selected_item, });
});

$(document).on("click", ".delete_card", function() {
    var card_id = $(this).parent().parent().attr("iid");
    Dajaxice.techdata.deleteHeatTreatCard(refresh, {"card_id": card_id, });
});
