$(document).ready(refresh);
$("#card_open").click(refresh);
function refresh() {
    var iid = $("#div_card").attr("iid")
    var card_type = $("#id_card_type").val();
    Dajaxice.techdata.getTransferCard(refreshCallBack, {"iid": iid, "card_type": card_type,});
}
function refreshCallBack(data) {
    $("#div_card").html(data);
}

new AutoSave(".word_textarea", Dajaxice.techdata.saveProcessRequirement).init();

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
        $(".form-search").hide();
        click_span.html(data.mark_user);
        $(click_span.attr("date-fill")).html(data.mark_date);
    }
    else {
        alert(data.warning);
    }
}
