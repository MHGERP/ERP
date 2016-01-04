$(document).ready(refresh);



function refresh() {
    var id_work_order = $("#id_work_order").val();
    Dajaxice.techdata.getTechdataList(getTechdataListCallBack, {"id_work_order": id_work_order});
}
function getTechdataListCallBack(data) {
	
    $("#widget-content").html(data);
}

$("#order_search").click(function() {
	refresh();
});

$(document).on("click", "#index_search", function(){
	var index = $("#index").val();
	Dajaxice.techdata.getIndex(getIndexCallBack,{"index":index});

});

function getIndexCallBack(data) {
    $("#widget-content2").html(data);
}

$(document).on("click", "#update-process", function(){
	var problem_statement = $("#problem_statement").val();
	var advice_statement = $("#advice_statement").val();
	var materiel_name = $("input:radio:checked").val();
	Dajaxice.techdata.addProcessReview(addProcessReviewCallBack,{"problem_statement":problem_statement,
															     "advice_statement":advice_statement,
															     "materiel_name": materiel_name,});

});
function addProcessReviewCallBack(data) {
    refresh();
}