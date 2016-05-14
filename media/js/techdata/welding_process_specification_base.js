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

$(document).on("click", ".turnpage", function() {
    var page = $("#paginator_div").attr("page");
    var total_page = $("#paginator_div").attr("total_page");
    var id_work_order = $("#div_card").attr("id_work_order");
    if($(this).hasClass("next-page")) {
        if(page == total_page) alert("已到最后一页");
        else {
            getCard(id_work_order, parseInt(page) + 1);
        }
    }
    else {
        if(page == "1") alert("已到第一页");
        else {
            getCard(id_work_order, parseInt(page) - 1);
        }
    }
});
