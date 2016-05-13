$(document).ready(refreshAll);

function refreshAll() {
    refreshProductionList();
    refreshWorkOrderList();
}

function refreshProductionList() {
    Dajaxice.sell.getProductionList(
        function(data){
            $("#widget-box").html(data);
        },
        {
            "type" : "up",
        }
    );
};

function refreshWorkOrderList() {
    Dajaxice.sell.getWorkOrderList(
        function(data) {
            $("#workorder-box").html(data);
        },
        {

        }
    );
};

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
            refreshProductionList();
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
                refreshAll();
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

$(document).on("click", ".workorder_generate", function() {
    var pid = $(this).parent().parent().attr("iid");
    Dajaxice.sell.getWorkOrderForm(
        function(data) {
            $("#workorder_form").html(data);
            $("#workorder_modal").attr("pid", pid);
            $("#workorder_modal").modal("show");
        },
        {

        }
    );
});

$("#id_generate").click(function() {
    var pid = $("#workorder_modal").attr("pid");
    Dajaxice.sell.generateWorkOrder(
        function(data) {
            if(data.status == "ok") {
                alert("工作令生成成功！");
                $("workorder_modal").modal("hide");
                refreshAll();
            }
            else if(data.status == "err") {
                alert("产品尚未通过审核！");
            }
            else {
                $("#workorder_form").html(data.html);
            }
        },
        {
            "pid" : pid,
            "form" : $("#workorder_form").serialize(),
        }
    );
});

$(document).on("dblclick", ".workorder_row", function() {
    
});
