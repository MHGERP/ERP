$("#following_search").click(function(){
    var bidid =$("#search_input").val();
    Dajaxice.purchasing.searchPurchasingFollowing(search_purchasing_callback,{
        'bidid':bidid
    });
});

function search_purchasing_callback(data){
    $("#following_table").html(data.html);
}
