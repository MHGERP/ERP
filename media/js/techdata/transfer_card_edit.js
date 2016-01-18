$(document).ready(refresh);

function refresh() {
    var iid = $("#div_card").attr("iid");
    Dajaxice.techdata.getTransferCard(refreshCallBack, {"iid": iid});
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
    Dajaxice.techdata.transferCardMark(markCallBack, {"iid": iid, "step": step, });
});
function markCallBack(data) {
    if(data.ret) {
        click_span.html(data.mark_user);
        $(click_span.attr("date-fill")).html(data.mark_date);
    }
    else {
        alert(data.warning);
    }
}
