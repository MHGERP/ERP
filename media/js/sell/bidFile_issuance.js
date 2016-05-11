$(document).ready(refresh);

function refresh() {
    var url = window.location.href;
    var arr = url.split("/");
    var param = arr[arr.length - 1]
    //alert(param);
    Dajaxice.sell.getBidFile_issuance(
        function(data){
            $("#widget-box").html(data);
        },
        {
            "param" : param, 
        }
    );
}

$(document).on("click", ".btn-upload", function() {
    $("#group_type").val($(this).attr("group"));
    $("#id_product_input").val($(this).parent().parent().attr("iid"));
});

$("#btn-upload").click(function() {
    $("#upload_form").ajaxSubmit({
        url: "/sell/product_bidFile_back",
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
