function func() {
    var s = $('select option:selected').val();
    if (s == "0")
        alert("0");
    else if (s == "1")
        Dajaxice.techdata.boxOutBought(boxOutBoughtCallback, {"boxoutbought" : s});
    else if (s == "2")
        alert("2");
}

function boxOutBoughtCallback(data) {
   $("#detail_table").html(data);
}
