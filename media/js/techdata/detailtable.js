$(document).on("click", "#order_search", function(){
    //var s = $('select option:selected').val();
    var s = $("#table_select").val();
    var order = $('#id_work_order').val();
    if (s == "0")
        $("#detail_table").html("");
    else if (s == "1")
        Dajaxice.techdata.firstFeeding(tableCallback, {"order" : order});
    else if (s == "2")
        Dajaxice.techdata.principalMaterial(tableCallback, {"order" : order});
    else if (s == "3")
        Dajaxice.techdata.auxiliaryMaterial(tableCallback, {"order" : order});
    else if (s == "4")
        Dajaxice.techdata.weldList(tableCallback, {"order" : order});
    else if (s == "5")
        Dajaxice.techdata.weldQuota(tableCallback, {"order": order});
    else if (s == "6")
        Dajaxice.techdata.techBoxWeld(tableCallback, {"order" : order});
    else if (s == "7")
        Dajaxice.techdata.boxOutBought(tableCallback, {"order" : order});
});

function tableCallback(data) {
   $("#detail_table").html(data);
}
