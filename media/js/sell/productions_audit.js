$(document).ready(refresh);

function refresh() {
    Dajaxice.sell.getProductionList(
        function(data){
            $("#widget-box").html(data);
        },
        {
            "type" : "up",
        }
    );
}

$(document).on("click", ".bidfile_audit", function() {
    var pid = $(this).parent().parent().attr("iid");
    Dajaxice.sell.getBidFileForm(
        function(data) {
            $("#audit_form").html(data.html);
            $("#id_bid").val(data.bid);
            $("#audit_modal").modal("show");
        },
        {
            "group" : $(this).attr("group"),
            "pid" : pid,
        }
    );
});

$(document).on("click", "#id_save", function() {
    var bid = $("#id_bid").val();
    var sta = $("#id_status").val();
    Dajaxice.sell.saveBidFileStatus(
        function(data) {
            $("#audit_modal").modal("hide");
            refresh();
        },
        {
            "bid" : bid,
            "sta" : sta,
        }
    );
});

$(document).on("click", ".product_audit", function() {
    var pid = $(this).parent().parent().attr("iid");
    Dajaxice.sell.saveProductStatus(
        function(data) {
            if(data == "ok") {
                alert("审核通过！");
                refresh();
            }
            else {
                alert("还有招标文件审核未通过！");
            }
        },
        {
            "pid" : pid,
        }
    )
});
