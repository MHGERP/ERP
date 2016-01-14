$(document).ready(refresh);



function refresh() {
    var id_work_order = $("#id_work_order").val();
    Dajaxice.techdata.getTechdataList(getTechdataListCallBack, {"id_work_order": id_work_order});
}
function getTechdataListCallBack(data) {
	
    $("#widget-box").html(data);
}

$("#order_search").click(function() {
	refresh();
});

$(document).on("click", "#index_search", function(){
	var index = $("#index").val();
	Dajaxice.techdata.getIndex(getIndexCallBack,{"index":index});

});

function getIndexCallBack(data) {
    $("#widget-content2").html(data);
}

$(document).on("click", "#update-process", function(){
	var problem_statement = $("#problem_statement").val();
	var advice_statement = $("#advice_statement").val();
	var materiel_name = $("input:radio:checked").val();
	Dajaxice.techdata.addProcessReview(addProcessReviewCallBack,{"problem_statement":problem_statement,
															     "advice_statement":advice_statement,
															     "materiel_name": materiel_name,});

});
function addProcessReviewCallBack(data) {
    refresh();
}
var iid;
var name;
$(document).on("click", ".tr_materiel1", function() {
    iid = $(this).attr("iid");
    name = $(this).children('td').eq(0).html();
    fill(iid);
    
});
function fill(iid){
    $("#card_modal").attr("iid", iid);
    Dajaxice.techdata.getProcessReviewForm(getProcessReviewFormCallback, {"iid" : iid});
}

function getProcessReviewFormCallback(data) {
    $("#materiel_div").html(data);
    $("#card_modal").modal();
    $("#material_name").html(name);
}

$(document).on("click","#save_process_btn", function(){
    
    Dajaxice.techdata.updateProcessReview(updateProcessReviewCallBack, 
                                    {
                                        'iid' : iid,
                                        'processReview_form' :$("#processReview_form").serialize(),
                                        
                                    });
});

function updateProcessReviewCallBack(data) {
	if(data == "ok") {
        alert("修改成功！");
        refresh();					
    }
    else {
        alert("修改失败！");
    }
}

$("#id_goto_next").click(function() {
    var cur_iid = $("#card_modal").attr("iid");
    var row = $("tr[iid='" + cur_iid + "']");
    var row_next = row.next(".tr_materiel1");
    name = $(row_next).children('td').eq(0).html();
    if(!row_next.html()) alert("本条为最后一条！");
    else fill(row_next.attr("iid"));
});

$("#id_goto_prev").click(function() {
    var cur_iid = $("#card_modal").attr("iid");
    var row = $("tr[iid='" + cur_iid + "']");
    var row_prev = row.prev(".tr_materiel1");
    name = $(row_prev).children('td').eq(0).html();
    if(!row_prev.html()) alert("本条为第一条！");
    else fill(row_prev.attr("iid"));
});
