function entry_confirm(eid){
    
}

var mid;
function change_item(itemid){
    mid = itemid;
    var a = $("tr#mid").find("td");
    for( var i = 8 ; i <= 10 ; i++ ){
        alert(a.eq(i).text());
    }

}

