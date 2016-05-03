$(document).ready(refresh);
$("#order_search").click(refresh);
function refresh() {
    var id_work_order = $("#id_work_order").val();
    $("#work_order").val(id_work_order);
    Dajaxice.techdata.getDesignBOM(refreshCallBack, {"id_work_order" : id_work_order, });
}
function refreshCallBack(data) {
    if(data.read_only) {
        $("#save_desginBOM_btn").hide();
    }
    else {
        $("#save_desginBOM_btn").show();
    }
    $("#widget-box").html(data.html);
}

//$("#designBOM_table tbody tr").click(function(){
//    alert("cao");
//    Dajaxice.techdata.getDesignBOMForm(getDesignBOMFormCallback, {});
//});

function fill(iid) {
    $("#designBOM_edit_modal").attr("iid", iid);
    Dajaxice.techdata.getDesignBOMForm(getDesignBOMFormCallback, {"iid" : iid});
}

$(document).on("click", "#designBOM_table tbody tr", function(){
    var iid = $(this).attr("iid");
    fill(iid);
});

function getDesignBOMFormCallback(data) {
    $("#materiel_div").html(data.materiel_form);
    $("#circulationroute_div").html(data.circulationroute_form);
    $("#designBOM_edit_modal").modal();
}

$(document).on("click","#save_desginBOM_btn", function(){
    var iid = $("#designBOM_edit_modal").attr("iid");
    //alert(iid);
    Dajaxice.techdata.saveDesignBOM(saveDesignBOMCallback, 
                                    {
                                        'iid' : iid,
                                        'materiel_form' :$("#materiel_form").serialize(),
                                        'circulationroute_form' : $("#circulationroute_form").serialize()
                                    });
});

function refreshSingleRow() {
    var iid = $("#designBOM_edit_modal").attr("iid");
    Dajaxice.techdata.getSingleDesignBOM(refreshSingleRowCallBack, {"iid" : iid})
}

function refreshSingleRowCallBack(data) {
    var cur_iid = $("#designBOM_edit_modal").attr("iid");
    var row = $("tr[iid='"+ cur_iid +"']");
    row.html(data);
}

function saveDesignBOMCallback(data) {
    if(data.status == "ok") {
        refreshSingleRow();
        alert("修改成功！");
    }
    else {
        if(data.circulationroute_error == "1")
            alert("流转路线必须连续");
        if(data.materiel_error == "1")
            alert("#materiel_div").html(data.html);
    }
}

$("#id_goto_next").click(function(){
   var cur_iid = $("#designBOM_edit_modal").attr("iid");
   var row = $("tr[iid='" + cur_iid + "']");
   var row_next = row.next(".designBOM_row");
   if(!row_next.html()) alert("本条为最后一条");
   else fill(row_next.attr("iid"));
});

$("#id_goto_prev").click(function(){
   var cur_iid = $("#designBOM_edit_modal").attr("iid");
   var row = $("tr[iid='" + cur_iid + "']");
   var row_prev = row.prev(".designBOM_row");
   if(!row_prev.html()) alert("本条为第一条");
   else fill(row_prev.attr("iid"));
})

$(document).on("click", "#btn_write_confirm", function() {
    var id_work_order = $("#id_work_order").val();   
    Dajaxice.techdata.designBOMWriterConfirm(writerConfirmCallBack, {"id_work_order": id_work_order})
});
function writerConfirmCallBack(data) {
    if(data.ret) {
        $("#btn_write_confirm").removeClass("btn-primary").addClass("btn-warning").html("编制完成");
        $("#span_write").html("编制人：" + data.user);
    }
}

$(document).on("click", "#btn_review_confirm", function() {
    var id_work_order = $("#id_work_order").val();   
    Dajaxice.techdata.designBOMReviewerConfirm(reviewerConfirmCallBack, {"id_work_order": id_work_order})
});
function reviewerConfirmCallBack(data) {
    if(data.ret) {
        $("#btn_review_confirm").removeClass("btn-primary").addClass("btn-warning").html("审核完成");
        $("#span_review").html("审核人：" + data.user);
    }
    else {
        alert("未完成编制，无法审核！");
    }
}



$("#btn-upload").click(function() {
    $("#upload_form").ajaxSubmit({
        url: "/techdata/BOMadd",
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
