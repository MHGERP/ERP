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

$(document).on("dblclick", ".step_area", function() {
    Dajaxice.techdata.getWeldStepList(function(data) {
        $("#process_table2").html(data);
        $("#process_modal2").modal("show");
    }, {
        "wwi_id": $("#div_card").attr("wwi_id"),
    });
});


$("#btn_save_process2").click(function() {
    var arr = new Array();
    $(".tr_process2").each(function() {
        var pid = $(this).attr("pid");
        var layer = $(this).find("input:eq(0)").val();
        var weld_method = $("#id_select").val();
        var name = ""
        var diameter = "";
        var polarity = $(this).find("input:eq(4)").val();
        var electric = $(this).find("input:eq(5)").val();
        var arc_voltage = $(this).find("input:eq(6)").val();
        var weld_speed = $(this).find("input:eq(7)").val();
        var heat_input = $(this).find("input:eq(8)").val();
        var remark = $(this).find("input:eq(9)").val();
        arr.push({

            "pid": pid,
            "layer": layer,
            "weld_method": weld_method,
            "name": name,
            "diameter": diameter,
            "polarity": polarity,
            "electric": electric,
            "arc_voltage": arc_voltage,
            "weld_speed": weld_speed,
            "heat_input": heat_input,
            "remark": remark,

        });
    });
    Dajaxice.techdata.saveWeldStep(function(data) {
        alert("保存成功！");
        refresh();
    }, {
        "arr": arr,
    });
});