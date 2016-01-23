$(document).ready(refresh);

function refresh() {
    var card_id = $(".widget-content").attr("card_id");
    Dajaxice.techdata.getHeatTreatCardDetail(function(data) {
        $(".widget-content").html(data);
    }, {"card_id": card_id, });
}

var click_span;

$(document).on("click", ".btn-mark", function() {
    click_span = $(this).parent();
    var step = $(this).attr("args");
    var card_id = $(".widget-content").attr("card_id");
    Dajaxice.techdata.heatTreatCardMark(markCallBack, {"card_id": card_id, "step": step});
});
function markCallBack(data) {
    if(data.ret) {
        click_span.html(data.mark_user);
        if(data.file_index) {
            $("#span-fileindex").html(data.file_index);
        }
    }
    else {
        alert(data.warning);
    }
}

function save_func(callback, thisElement) {
    var attr = thisElement.attr("args");
    var card_id = $(".widget-content").attr("card_id");
    var content = thisElement.html();
    Dajaxice.techdata.heatTreatCardVariableSave(function() {}, {"attr": attr, "card_id": card_id, "content": content});
    callback();
}
new AutoSave(".word_textarea", save_func, 500).init();
