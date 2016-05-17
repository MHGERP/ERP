$(document).ready(function(){
    $(document).on("click", "#saveWeldDataBtn", function(){
        var temp = $("#temp").val();
        var humi = $("#humi").val();
        var reg = /^[0-9]+$/;
        if(reg.test(temp) && reg.test(humi)){
            Dajaxice.storage.weldDemandDataUpdate(weldDemandDataUpdataCallback, {"temp":parseInt(temp),"humi":parseInt(humi)});
        }
    })
})
function weldDemandDataUpdataCallback(data){
    alert(data.message);
}
