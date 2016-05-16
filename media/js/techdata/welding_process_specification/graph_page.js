$(document).on("dblclick", "#pic_area", function() {
    $("#id_input").val($("#div_card").attr("id_work_order"));
    $("#pic_modal").modal("show");
});

$(document).on("click", "#btn_save_pic", function() {
     $("#pic_form").ajaxSubmit({
        url: "/techdata/weldingProcessSpecificationPicUpload",
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
                $("#pic_modal").modal("hide");
            }
        }
    });
});
