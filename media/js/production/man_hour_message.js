$(document).ready(refresh);
function refresh(){
    Dajaxice.production.getHourSearch(getHourSearchCallBack,{"form":$("#hourMessageSearchForm").serialize()});
}
$(document).on("click","#btn-search",function(){
    refresh();
})

function getHourSearchCallBack(data){
    $("#widget-content").html(data);
}