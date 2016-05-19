$(document).ready(refresh);

function refresh() {
    var wwi_id = $("#div_card").attr("wwi_id");
    Dajaxice.techdata.getCard(function(data){
        $("#div_card").html(data);
    },{"wwi_id":wwi_id});
}

$(document).on("dblclick", ".process_area", function() {
    Dajaxice.techdata.getWeldingWorkInstructionProcessList(function(data) {
        $("#process_table").html(data);
        $("#process_modal").modal("show");
    }, {
        "wwi_id": $("#div_card").attr("wwi_id"),
    });
});

$("#btn_save_process").click(function() {
    var arr = new Array();
    $(".tr_process").each(function() {
        var pid = $(this).attr("pid");
        var index = $(this).find("input:eq(0)").val();
        var name = "";
        var detail = $(this).find("textarea:eq(0)").val();
        arr.push({
            "pid": pid,
            "index": index,
            "name": name,
            "detail": detail,
        });
    });
    Dajaxice.techdata.saveWeldWorkInstructionProcess(function(data) {
        alert("保存成功！");
        refresh();
    }, {
        "arr": arr,
    });
});