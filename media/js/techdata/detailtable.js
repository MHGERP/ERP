function func() {
    var s = $('select option:selected').val();
    if (s == "0")
        return;
    else if (s == "1")
        Dajaxice.techdata.boxOutBought(boxOutBoughtCallback, {"boxoutbought" : s});
    else if (s == "2")
        alert("2");
    else if (s == "3")
        alert("3");
    else if (s == "4")
        alert("4");
    else if (s == "5")
        alert("5");
    else if (s == "6")
        alert("6");
    else if (s == "7")
        alert("7");
    else if (s == "8")
        alert("8");
}

function boxOutBoughtCallback(data) {
   $("#detail_table").html(data);
}
