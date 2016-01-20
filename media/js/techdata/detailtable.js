$(document).on("click", "#order_search", function(){
    //var s = $('select option:selected').val();
    var s = $("#table_select").val();
    var order = $('#id_work_order').val();
    if (s == "0")
        $("#detail_table").html("");
    else if (s == "1")
        Dajaxice.techdata.firstFeeding(tableCallback, {"order" : order});
    else if (s == "2")
        Dajaxice.techdata.principalMaterial(tableCallback, {"order" : order});
    else if (s == "3")
        Dajaxice.techdata.auxiliaryMaterial(tableCallback, {"order" : order});
    else if (s == "4")
        Dajaxice.techdata.weldList(tableCallback, {"order" : order});
    else if (s == "5")
        Dajaxice.techdata.weldQuota(tableCallback, {"order": order});
    else if (s == "6")
        Dajaxice.techdata.techBoxWeld(tableCallback, {"order" : order});
    else if (s == "7")
        Dajaxice.techdata.boxOutBought(tableCallback, {"order" : order});
});

function tableCallback(data) {
   $("#detail_table").html(data);
}

var iid;
var categories;
$(document).on("click", ".tr_materiel", function() {
    iid = $(this).attr("iid");
    categories = $(this).attr("cid");
    fill(iid);
});

function fill(iid) {
    $("#card_modal").attr("iid", iid);
    Dajaxice.techdata.getAuxiliaryMaterielInfo(getInfoCallBack, {"iid": iid,
                                                                 "categories":categories});
}

function getInfoCallBack(data) {
    $("#type_in").html(data);
}

$(document).on("click","#id_success",function(){
    $("#id_quota").val(($("#id_total_weight").val()*$("#id_quota_coefficient").val()).toFixed(6));
    $("#use_ratio").val(($("#id_net_weight").val()/$("#id_quota").val()).toFixed(5));

});

 $(document).on("click","#id_confirm",function(){
   var categorie = $("#id_categorie_type").val();
   $('#id_categorie_type').attr('disabled',false);
   $('#id_material').attr('disabled',false);
    Dajaxice.techdata.saveAuxiliaryMaterielInfo(saveAuxiliaryMaterielInfoCallBack, {"iid": iid,
                                                                                    "categories":categorie,
                                                                                    "auxiliary_material_form":$("#auxiliary_material_form").serialize()});
 });
 function saveAuxiliaryMaterielInfoCallBack(data){
    if(data == "ok") {
        alert("修改成功！");
        $('#id_categorie_type').attr('disabled',true);
        $('#id_material').attr('disabled',true);
        var order = $('#id_work_order').val();
         Dajaxice.techdata.auxiliaryMaterial(tableCallback, {"order" : order});               
    }
    else {
        alert("修改失败！");
    }
 }
$("#id_goto_next").click(function(){
   var cur_iid = $("#card_modal").attr("iid");
   var row = $("tr[iid='" + cur_iid + "']");
   var row_next = row.next(".tr_materiel");
   categories = $(row_next).attr("cid");
   if(!row_next.html()) alert("本条为最后一条");
   else fill(row_next.attr("iid"));
});

$("#id_goto_prev").click(function(){
   var cur_iid = $("#card_modal").attr("iid");
   var row = $("tr[iid='" + cur_iid + "']");
   var row_prev = row.prev(".tr_materiel");
   categories = $(row_prev).attr("cid");
   if(!row_prev.html()) alert("本条为第一条");
   else fill(row_prev.attr("iid"));
});

$(document).on("click", "#btn_write_confirm", function() {
    var order = $('#id_work_order').val();
    Dajaxice.techdata.boxOutBoughtWriteConfirm(writeConfirmCallback, {"id_work_order" : order});
});

function writeConfirmCallback(data) {
    $("#span_write").html("编制人：" + data.user);
}

$(document).on("click", "#btn_review_confirm", function() {
    var order = $('#id_work_order').val();
    Dajaxice.techdata.boxOutBoughtReviewConfirm(reviewConfirmCallback, {"id_work_order" : order});
});

function reviewConfirmCallback(data) {
    $("#span_review").html("审核人：" + data.user);
}
