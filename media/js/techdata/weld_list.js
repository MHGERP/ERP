var jointArray = Array();

$(document).ready(refresh);
$("#order_search").click(refresh);

function refresh() {
   // alert("我要刷新了！");
    var id_work_order = $("#id_work_order").val();
    Dajaxice.techdata.getWeldSeamList(refreshCallBack, {"id_work_order": id_work_order, });
}
function refreshCallBack(data) {
    if(data.read_only) {
        $("#id_save").hide();
        $("#id_calculate").hide();
    }
    else {
        $("#id_save").show();
        $("#id_calculate").show();
    }
    $("#widget-box").html(data.html);
}
function refreshSingleRow() {
    var iid = $("#card_modal").attr("iid");
    Dajaxice.techdata.getSingleWeldSeamInfo(refreshSingleCallBack, {"iid": iid})
}
function refreshSingleCallBack(data) {
    var cur_iid = $("#card_modal").attr("iid");
    var row = $("tr[iid='" + cur_iid + "']");
    row.html(data);
}
$(document).on("dblclick", ".tr_materiel td", function() {
    if($(this).index() != 0) {
        var iid = $(this).parent().attr("iid");
        fill(iid);
        $("#card_modal").modal();
    }
});

function fill(iid) {
    $("#card_modal").attr("iid", iid);
    Dajaxice.techdata.getWeldSeamCard(getCardCallBack, {"full": true, "iid": iid});
}
function getCardCallBack(data) {
    $("#weld_seam_card").html(data);
}

$("#id_save").click(function() {
    var iid = $("#card_modal").attr("iid");
    Dajaxice.techdata.modifyWeldSeam(saveCallBack, {"iid": iid, "form": $("#weld_seam_card").serialize()})
});
function saveCallBack(data) {
    if(data == "ok") {
        refreshSingleRow();
        alert("焊缝信息修改成功！");
    }
    else {
        $("#weld_seam_card").html(data);
    }
}

$("#id_goto_next").click(function() {
    var cur_iid = $("#card_modal").attr("iid");
    var row = $("tr[iid='" + cur_iid + "']");
    var row_next = row.next(".tr_materiel");
    if(!row_next.html()) alert("本条为最后一条！");
    else fill(row_next.attr("iid"));
});

$("#id_goto_prev").click(function() {
    var cur_iid = $("#card_modal").attr("iid");
    var row = $("tr[iid='" + cur_iid + "']");
    var row_prev = row.prev(".tr_materiel");
    if(!row_prev.html()) alert("本条为第一条！");
    else fill(row_prev.attr("iid"));
});

$(document).on("click", "#btn_write_confirm", function() {
    var id_work_order = $("#id_work_order").val();   
    Dajaxice.techdata.weldListWriterConfirm(writerConfirmCallBack, {"id_work_order": id_work_order})
});
function writerConfirmCallBack(data) {
    if(data.ret) {
        $("#span_write").html("编制人：" + data.user);
    }
}

$(document).on("click", "#btn_review_confirm", function() {
    var id_work_order = $("#id_work_order").val();   
    Dajaxice.techdata.weldListReviewerConfirm(reviewerConfirmCallBack, {"id_work_order": id_work_order})
});
function reviewerConfirmCallBack(data) {
    if(data.ret) {
        $("#span_review").html("审核人：" + data.user);
    }
    else {
        alert("未完成编制，无法审核！");
    }
}

function clearCheckBox() {
    var index;
    for(var i = 0; i < jointArray.length; ++i) {
        index = jointArray[i];
        $(":checkbox[arg='"+index+"']:first").attr("checked", false);
    }
}

$("#test").click(function(){
    clearCheckBox();
});

$("#joint_btn").click(function(){
   jointArray = Array();
   var method = null, thin1 = null, thin2 = null;
   var child;
   $("input.checkbox").each(function(){
        if(this.checked) {
            //alert($(this).parent().parent().children().eq(5).text());
            child = $(this).parent().parent().children();
            if(method == null) {
                method = child.eq(5).text();
                thin1 = child.eq(6).text();
                thin2 = child.eq(7).text();
            }
            else if(method != child.eq(5).text() || thin1 != child.eq(6).text() || thin2 != child.eq(7).text()) {
                alert("所选焊缝不能合并");
                jointArray = Array();
                clearCheckBox();
                return;
            }
            jointArray.push($(this).attr("arg"));
         }
   });
    /*Dajaxice.techdata.addToJointDetail(
        add_to_jointdetail_callback, 
        {
            "id_work_order" : $("#id_work_order".val(),
            "jointArray" : jointArray,
        }
    );*/
});

function add_to_jointdetail_callback(data) {
    
}
