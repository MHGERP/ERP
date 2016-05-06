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

function clear(){
  $("#status").val("");
  $("#plan_date").val("");
}


$(document).on("click", "#workorder_search_form .btn", function() {
  Dajaxice.production.workorderSearch(workorderSearchCallBack, {"form": $("workorder_search_form").serialize()});
});

function workorderSearchCallBack(data){
  $("#select_table").html(data.html);
}

$(document).on("click","#workadd", function(){
  $(document).find("#workSearch").val("");
  Dajaxice.production.workorderSearch(workorderSearchCallBack, {"workSearchText":$("#workSearch").val()});
});

$(document).on("click", "#work_confirm_btn",function(){
  var workList = $("#select_table tbody").children("tr");
  var checkList = new Array();
  $(workList).each(function(i){
    var tt = $(this).find("td:eq(0)").children().eq(0);
    //alert(tt.attr("checked"));
    if(tt.attr("checked")==="checked"){
      checkList.push($(this).children("td").eq(1).text());
    }
  });
  //alert(checkList);
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



$(document).on("click","#test", function(){
  var statu = $(this).parents("tr").children("td").eq(8).text();
  var plandate = $(this).parents("tr").children("td").eq(9).attr("plandate");
  alert(statu + ", " + plandate);
});


$(document).on("click", "#prodplan_update_bt", function(){
  //clear();
  planid = $(this).parents("tr").attr("planid");
  var statu = $(this).parents("tr").children("td").eq(8).attr("statu");    
  var plandate = $(this).parents("tr").children("td").eq(9).attr("plandate");
  $("#update_form")[0].reset();
  var optionList = $("#update_form").find("[name=status]").children();
  $(optionList).each(function(){
    if($(this).attr("selected")=="selected"){
      $(this).removeAttr("selected");
    }
  });
  $(optionList).each(function(){
    if($(this).attr("value")==statu){
      $(this).attr("selected","selected");
    }
  });
  $("#update_form").find("[name=plan_date]").val(plandate);
});


$(document).on("click", "#prodplan_confirm_btn", function(){
  Dajaxice.production.prodplanUpdate(prodplanUpdateCallBack, {"form":$("#update_form").serialize(), "planid":planid});
});

function prodplanUpdateCallBack(data){
  $("#prodplan_table").html(data.html);
  $("#prodplan_modify_modal").modal("hide");
  alert(data.message);
}

$(function(){
  $("#plan_date").datetimepicker({format:"yyyy-mm-dd",minView:2,autoclose:true});
  var myDate = new Date();
  //alert(myDate.toLocaleDateString());
  $("#plan_date").datetimepicker("setStartDate",myDate.toLocaleDateString());
});


$(document).on("click", "#productionplan_search_form .btn", function(){
  Dajaxice.production.prodplanSearch(prodplanSearchCallBack, {"form":$("#productionplan_search_form").serialize()});
});

function prodplanSearchCallBack(data) {
  $("#prodplan_table").html(data.html);
}
