$(document).ready(function() {
    var card_type = $("#id_card_type").val();   
    if(!card_type) {
        refresh();
    }
});
$("#card_open").click(function() {
    Dajaxice.techdata.createTransferCard(refresh, {
        "iid": $("#div_card").attr("iid"),
        "card_type": $("#id_card_type").val(),   
    });
    $(".form-search").hide();
});
function refresh() {
    var iid = $("#div_card").attr("iid")
    var page = $("#paginator_div").attr("page");
    getCard(iid, page);
}

function getCard(iid, page) {
    Dajaxice.techdata.getTransferCard(function(data) {
        $("#div_card").html(data);
    }, {
        "iid": iid,
        "page": page,
    });
}

$(document).on("dblclick", ".info_area", function() {
    Dajaxice.techdata.getTransferCardInfoForm(function(data) {
        $("#info_card").html(data);
        $("#info_modal").modal("show");
    }, {
        "iid": $("#div_card").attr("iid"),
    });
});

$(document).on("click", ".turnpage", function() {
    var page = $("#paginator_div").attr("page");
    var total_page = $("#paginator_div").attr("total_page");
    var iid = $("#div_card").attr("iid")
    if($(this).hasClass("next-page")) {
        if(page == total_page) alert("已到最后一页");
        else {
            getCard(iid, parseInt(page) + 1);
        }
    }
    else {
        if(page == "1") alert("已到第一页");
        else {
            getCard(iid, parseInt(page) - 1);
        }
    }
});
$("#btn_save_info").click(function() {
    Dajaxice.techdata.saveTransferCardInfoForm(function(data) {
        if(data.ret == "ok") {
            alert("保存成功");
            refresh();
            $("#info_modal").modal("hide");
        }
        else {
            $("#info_card").html(data.html);
        }
    }, {
        "iid": $("#div_card").attr("iid"),
        "form": $("#info_card").serialize(),
    })
});

$(document).on("dblclick", ".process_area", function() {
    Dajaxice.techdata.getTransferCardProcessList(function(data) {
        $("#process_table").html(data);
        $("#process_modal").modal("show");
    }, {
        "iid": $("#div_card").attr("iid"),
    });
});
$("#btn_save_process").click(function() {
    var arr = new Array();
    $(".tr_process").each(function() {
        var pid = $(this).attr("pid");
        var index = $(this).find("input:eq(0)").val();
        var name = $(this).find("input:eq(1)").val();
        var detail = $(this).find("textarea:eq(0)").val();
        arr.push({
            "pid": pid,
            "index": index,
            "name": name,
            "detail": detail,
        });
    });
    Dajaxice.techdata.saveTransferCardProcess(function(data) {
        alert("保存成功！");
        refresh();
    }, {
        "arr": arr,
    });
});
$(document).on("dblclick", ".pic_area", function() {
    $("#iid_input").val($("#div_card").attr("iid"));
    $("#pic_modal").modal("show");
});
$("#btn_save_pic").click(function() {
    $("#pic_form").ajaxSubmit({
        url: "/techdata/transferCardPicUpload",
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
})
var click_span;

$(document).on("click", ".btn-mark", function() {
    click_span = $(this).parent();
    var step = $(this).attr("args");
    var iid = $("#div_card").attr("iid");
    Dajaxice.techdata.transferCardMark(markCallBack, {"iid": iid, "step": step,});
});
function markCallBack(data) {
    if(data.ret) {
        if(data.file_index) {
            $("#file_index_span").html(data.file_index)
        }
        click_span.html(data.mark_user);
        $(click_span.attr("date-fill")).html(data.mark_date);
    }
    else {
        alert(data.warning);
    }
}


//for print test
$(document).on("click", "#btn_print", function() {
    var iid = $("#div_card").attr("iid")
    var page = $("#paginator_div").attr("page");
    Dajaxice.techdata.getTransferCard(function(data) {
        var bodyHTML = window.document.body.innerHTML;
        window.document.body.innerHTML = data;
        window.print();
        window.document.body.innerHTML = bodyHTML;
    }, {
        "iid": iid,
        "page": page,
        "is_print": true,
    });
    
});
