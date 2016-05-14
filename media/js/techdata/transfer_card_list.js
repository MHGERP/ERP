$(document).ready(function() {
    Dajaxice.techdata.getTransferCardList(function(data) {
        $("#widget-box").html(data);
    }, {
        "id_work_order": $("#widget-box").attr("id_work_order"),
    })
})
