$("#following_search").click(function(){
    var bidid =$("#search_input").val();
    Dajaxice.purchasing.searchPurchasingFollowing(search_purchasing_callback,{
        'bidid':bidid
    });
});

function search_purchasing_callback(data){
    $("#following_table").html(data.html);
}

function check_arrival(bid){
    Dajaxice.purchasing.checkArrival(check_arrival_callback,{'bid':bid});}

function check_arrival_callback(data){
    $("#arrival_table_div").html(data.arrival_table_html);
}

function change_arrival_status(){
}
