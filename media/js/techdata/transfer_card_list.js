$(document).ready(refresh);

function refresh() {
    Dajaxice.techdata.getTransferCardList(function(data) {
        $("#widget-box").html(data);
    }, {
        "id_work_order": $("#widget-box").attr("id_work_order"),
    });
}
$(document).on("click", ".btn-remove", function() {
    var iid = $(this).parent().parent().attr("iid");
    if(confirm("您确定删除此流转卡？"))  {
        Dajaxice.techdata.removeTransferCard(refresh, {
            "iid": iid,
        })
    };
});
