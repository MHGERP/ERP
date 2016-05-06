$("#id_plan_date__gte").datetimepicker({
    format : 'yyyy-mm-dd',
    minView : 2,
    autoclose : true,
});

$("#id_plan_date__lte").datetimepicker({
  format : 'yyyy-mm-dd',
  minView : 2,
  autoclose : true,
});

$(document).on("click", "#workorder_search_form .btn", function() {
  Dajaxice.production.workorderSearch(workorderSearchCallBack, {"form": $("#workorder_search_form").serialize()});
});

$(document).on("click","#workadd", function(){
  $(document).find("#id_order_index__contains").val("");
  Dajaxice.production.workorderSearch(workorderSearchCallBack, {"form": $("#workorder_search_form").serialize()});
});

function workorderSearchCallBack(data){
  $("#select_table").html(data.html);
}



$(document).on("click", "#work_confirm_btn",function(){
  var workList = $("#select_table tbody").children("tr");
  var checkList = new Array();
  $(workList).each(function(i){
    var tt = $(this).find("td:eq(0)").children().eq(0);
    if(tt.attr("checked")==="checked"){
      checkList.push($(this).children("td").eq(1).text());
    }
  });
  Dajaxice.production.workorderAdd(workorderAddCallBack,{"checkList":checkList});
});

function workorderAddCallBack(data){
  $("#prodplan_table").html(data.html);
}

var planid;
$(document).on("click", "#prodplan_delete_btn", function(){
  var temp = confirm("删除不可恢复");
  if(temp == true){
    planid = $(this).parents("tr").attr("planid");
    Dajaxice.production.prodplanDelete(prodplanDeleteCallBack, {"planid":planid});
  }
});

function prodplanDeleteCallBack(data){
  $(document).find("tr[planid="+ planid +"]").remove();
}

var updateplanid = "";
$(document).on("click", "#prodplan_update_btn", function(){
  updateplanid = $(this).parents("tr").attr("planid");
  Dajaxice.production.getProductPlanForm(getProductplanFormCallBack, {"planid": updateplanid});
});
function getProductplanFormCallBack(data){
  $("#productionplan_update_div").html(data);
  $("#plan_date").datetimepicker({format:"yyyy-mm-dd",minView:2,autoclose:true});
  $("#prodplan_modify_modal").modal("show");
}


$(document).on("click", "#prodplan_confirm_btn", function(){
  Dajaxice.production.prodplanUpdate(prodplanUpdateCallBack, {"form":$("#productionplan_update_form").serialize(), "planid": updateplanid});
});

function prodplanUpdateCallBack(data){
  $("#prodplan_table").html(data.html);
  $("#prodplan_modify_modal").modal("hide");
  alert(data.message);
}


$(document).on("click", "#productionplan_search_form .btn", function(){
  Dajaxice.production.prodplanSearch(prodplanSearchCallBack, {"form":$("#productionplan_search_form").serialize()});
});

function prodplanSearchCallBack(data) {
  $("#prodplan_table").html(data.html);
}
