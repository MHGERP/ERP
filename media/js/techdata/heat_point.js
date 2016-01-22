$(document).ready(refresh);

function refresh() {
    var card_id = $(".widget-content").attr("card_id");
    Dajaxice.techdata.getHeatPointDetail(function(data) {
        $(".widget-content").html(data);
    }, {"card_id": card_id, });
}

$(document).on("click", "#writer", function() {
    var card_id = $(".widget-content").attr("card_id");
    Dajaxice.techdata.heatTreatmentArrangementWrite(heatTreatmentArrangementWriteCallback, {"card_id" : card_id});
});

function heatTreatmentArrangementWriteCallback(data) {
    $("#bianhao").html("RR02-"+data.bianhao);
    $("#writer").removeClass();
    $("#writer").html(data.writer);
}

$(document).on("click", "#reviewer", function() {
    var card_id = $(".widget-content").attr("card_id");
    Dajaxice.techdata.heatTreatmentArrangementReview(heatTreatmentArrangementReviewCallback, {"card_id" : card_id});
});

function heatTreatmentArrangementReviewCallback(data) {
    if (data.res) {
        $("#reviewer").removeClass();
        $("#reviewer").html(data.reviewer);
    }
    else {
        alert("请先完成:工艺制定");
    }
}
$(document).on("click", "#btn-upload", function() {
    var card_id = $(".widget-content").attr("card_id");
    $("#upload_form").ajaxSubmit({
        url: "/techdata/uploadHeatArrangement" + "?card_id=" + card_id,
        type: "POST",
        clearForm: true,
        resetForm: true,
        error: function(data) {
            alert("失败");
        },
        success: function(data) {
            //alert(data);
            $("#mypic").attr("src", data);
        }
    });
});
