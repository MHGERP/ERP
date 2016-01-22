function registDatepicker() {
    $('#date').datetimepicker({
        format : 'yyyy-mm-dd',
        autoclose : true,
        minView : 'month',
    });
}

$(document).ready(refresh);
$("#order_search").click(refresh);
function refresh() {
    var id_work_order = $("#id_work_order").val();
    Dajaxice.techdata.getTechPreparationPlan(refreshCallBack, {"id_work_order" : id_work_order});
}
function refreshCallBack(data) {
    $("#widget-box").html(data);
}

function fill(iid) {
    $("#techPlan_modal").attr("iid", iid);
    if(iid != -1) {
        $("#techPlan_modal").attr("addOrUpdate", "update");
    }
    else{
        $("#techPlan_modal").attr("addOrUpdate", "add");
    }
    Dajaxice.techdata.getTechPlanForm(getTechPlanFormCallBcak, {"iid" : iid});
}

function getTechPlanFormCallBcak(data) {
    $("#tech_preparation_plan_form").html(data);
    $("#techPlan_modal").modal();
    registDatepicker();
}

$(document).on("click", "#add_tech_plan", function(){
    fill(-1);
});


$(document).on("click", "#id_save", function(){
   var id_work_order =  $("#id_work_order").val();
   var iid = $("#techPlan_modal").attr("iid");
   //alert(id_work_order);
   var addOrUpdate = $("#techPlan_modal").attr("addOrUpdate");
   Dajaxice.techdata.saveTechPlan(saveTechPlanCallBack, {
       "id_work_order" : id_work_order,
       "tech_preparation_plan_form" : $("#tech_preparation_plan_form").serialize(),
       "addOrUpdate" : addOrUpdate,
       "iid" : iid,
   })
});

function saveTechPlanCallBack(data) {
    if(data.ret == "ok"){
        refresh();
        alert("保存成功");
    } 
    else {
        $("#tech_preparation_plan_form").html(data.form_html);
        alert("请检查输入");
    }
}

$(document).on("click", ".techPlan_row", function(){
    var iid = $(this).attr("iid");
    fill(iid);
});
