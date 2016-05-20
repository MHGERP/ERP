var stop_card_type;
var stop_role;
var refundid;
$(document).ready(function(){
    $(document).on("click","span[name='storage_stop_btn']",function(){
        stop_card_type = $(this).attr("card_type");
        stop_role = $(this).attr("role");
        refundid =  $(this).attr("fid");
        $("#cardStatusStop").modal('show');        
    })
    $(document).on("click","#card_status_stop_save",function(){
        if(confirm("请仔细确认，一旦终止将无法恢复")){
            var form = $("#card_status_form").serialize();
            Dajaxice.storage.cardStatusStop(cardstatusstop_callback,{"stop_card_type":stop_card_type,"stop_role":stop_role,"form":form,"fid":refundid});
        }
    })
})

function cardstatusstop_callback(data){
    $("#card_status_form").html(data.form_html);
    alert(data.message);
}
