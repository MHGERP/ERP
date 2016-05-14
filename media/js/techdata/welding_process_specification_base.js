$(document).ready(refresh);

function refresh() {
    var id_work_order = $("#div_card").attr("id_work_order");
    var page = $("#paginator_div").attr("page");
    getCard(id_work_order, page);
}
function getCard(id_work_order, page) {
    Dajaxice.techdata.getWeldingProcessSpecification(function(data) {
        $("#div_card").html(data);
    }, {
        "id_work_order": id_work_order,
        "page": page,
    });
}
