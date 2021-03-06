$(document).ready(refresh);

function refresh() {
    Dajaxice.techdata.getExcuteList(refreshCallBack, {});
}
function refreshCallBack(data) {
    $(".widget-content").html(data);
}

$(document).on("click", ".btn-upload", function() {
    $("#id_execute_input").val($(this).parent().parent().attr("iid"));
});

$(document).on("click", ".search-choice-close", function() {
    var pid = $(this).attr("pid");
    var parent_node = $(this).parent();
    Dajaxice.techdata.removeProgram(function(data) {
        if(data.ret) parent_node.remove();
        else {
            alert("后台出错！");
        }
    }, 
    {"pid": pid}
    );
});

$("#btn-upload").click(function() {
    $("#upload_form").ajaxSubmit({
        url: "/techdata/programadd",
        type: "POST",
        clearForm: true,
        resetForm: true,
        error: function(data) {
            
        },
        success: function(data) {
            if(data.file_upload_error == 2) {
                alert("上传失败，请重试");
            }
            else {
                refresh();
            }
        }
    });
})

$(document).on("click", ".btn-feedback", function() {
    $("#feedback_save").attr("args", $(this).parent().parent().attr("iid"));
})
$("#feedback_save").click(function() {
    var iid = $(this).attr("args");
    Dajaxice.techdata.saveProgramFeedback(saveFeedbackCallBack, {"form": $("#feedback_form").serialize(), "iid": iid});
});

function saveFeedbackCallBack(data) {
    if(data.ret) {
        refresh();
    }
    else {
        alert("保存失败，请重试");
    }
}
