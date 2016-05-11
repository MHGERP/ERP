$(document).ready(function() {
    var card_type = $("#id_card_type").val();   
    if(!card_type) {
        refresh();
    }
});
$("#card_open").click(function() {
    Dajaxice.techdata.createTransferCard(refresh, {
        "iid": $("#div_card").attr("iid"),
        "card_type": $("#id_card_type").val(),   
    });
    $(".form-search").hide();
});
function refresh() {
    var iid = $("#div_card").attr("iid")
    Dajaxice.techdata.getTransferCard(refreshCallBack, {"iid": iid});
}
function refreshCallBack(data) {
    $("#div_card").html(data);
}


var click_span;

$(document).on("click", ".btn-mark", function() {
    click_span = $(this).parent();
    var step = $(this).attr("args");
    var iid = $("#div_card").attr("iid");
    var card_type = $("#id_card_type").val();
    Dajaxice.techdata.transferCardMark(markCallBack, {"iid": iid, "step": step, "card_type": card_type});
});
function markCallBack(data) {
    if(data.ret) {
        if(data.file_index) {
            $("#file_index_span").html(data.file_index)
        }
        click_span.html(data.mark_user);
        $(click_span.attr("date-fill")).html(data.mark_date);
    }
    else {
        alert(data.warning);
    }
}
