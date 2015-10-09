$(document).on("click", "#search_materielexecute", function(){
    var query_input = $("#input_materielexecute_search").val();
//    alert(query_input);
    Dajaxice.purchasing.MaterielExecuteQuery(materielexecute_query_callback, {"number":query_input});
});

function materielexecute_query_callback(data) {
    alert(data.materielexecute_html);
    $("#materielexecute_table").html(data.materielexecute_html);
}
