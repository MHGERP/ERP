$(document).ready(refresh);

function refresh() {
    Dajaxice.techdata.getWorkOrderOfConnectList(refreshCallBack, {});
}

function refreshCallBack(data) {
    $(".widget-content").html(data);
}
$(document).on("click", ".btn-upload", function() {
    $("#id_work_order_input").val($(this).parent().parent().attr("iid"));
});

$("#btn-upload").click(function() {
    $("#upload_form").ajaxSubmit({
        url: "/techdata/connectOrientationAdd",
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

$(document).on("click", ".search-choice-close", function() {
    var pid = $(this).attr("pid");
    var parent_node = $(this).parent();
    Dajaxice.techdata.removeConnectOrientation(function(data) {
        if(data.ret) parent_node.remove();
        else {
            alert("后台出错！");
        }
    }, 
    {"pid": pid}
    );
});
