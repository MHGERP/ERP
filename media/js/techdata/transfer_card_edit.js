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

function save_func(callback, thisElement) {
    var id = thisElement.attr("id");
    var content = thisElement.html();
    Dajaxice.techdata.saveProcessRequirement(function(){}, {"id": id, "content": content, });
    callback();
}
new AutoSave(".word_textarea", save_func, 1000).init();

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
