$(document).ready(refresh);

function refresh() {
    Dajaxice.sell.getProductionList(
        function(data){
            $("#widget-box").html(data);
        },
        {

        }
    );
}

function fill(iid) {
    if(iid == -1) {

    }
    Dajaxice.sell.getProductionForm(
        function(data) {
            $("#product_form").html(data);
            $("#product_modal").modal("show");
        },
        {
            "iid" : iid,
        }
    );
}

$(document).on("click", ".btn-upload", function() {
    $("#group_type").val($(this).attr("group"));
    $("#id_product_input").val($(this).parent().parent().attr("iid"));
});

$("#add_product").click(function(){
    fill(-1);
});

$("#id_save").click(function(){
    Dajaxice.sell.saveProduct(
        function(data) {
            alert("保存成功");
            $("#product_modal").modal("hide");
            refresh();
        },
        {
            "form" : $("#product_form").serialize(),
        }
    )
});

$("#btn-upload").click(function() {
    $("#upload_form").ajaxSubmit({
        url: "/sell/product_bidFile_add",
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
