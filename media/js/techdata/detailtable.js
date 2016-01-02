function func() {
    var s = $('select option:selected').val();
    if (s == "0")
        $("#detail_table").html("");
    else if (s == "1")
        Dajaxice.techdata.firstFeeding(tableCallback, {});
    else if (s == "2")
        Dajaxice.techdata.principalMaterial(tableCallback, {});
    else if (s == "3")
        Dajaxice.techdata.auxiliaryMaterial(tableCallback, {});
    else if (s == "4")
        Dajaxice.techdata.weldList(tableCallback, {});
    else if (s == "5")
        Dajaxice.techdata.weldQuota(tableCallback, {});
    else if (s == "6")
        Dajaxice.techdata.techBoxWeld(tableCallback, {});
    else if (s == "7")
        Dajaxice.techdata.boxOutBought(tableCallback, {});
}

function tableCallback(data) {
   $("#detail_table").html(data);
}
