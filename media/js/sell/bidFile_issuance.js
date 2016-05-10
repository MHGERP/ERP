$(document).ready(refresh);

function refresh() {
    var url = window.location.href;
    var arr = url.split("/");
    var param = arr[arr.length - 1]
    //alert(param);
    Dajaxice.sell.getBidFile_issuance(
        function(data){
            $("#widget-box").html(data);
        },
        {
            "param" : param, 
        }
    );
}
