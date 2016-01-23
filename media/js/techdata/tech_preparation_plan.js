function registDatepicker() {
    $('#date').datetimepicker({
        format : 'yyyy-mm-dd',
        autoclose : true,
        minView : 'month',
        todayBtn : true,
    });
}

$("#querydate").datetimepicker({
    format : 'yyyy-m',
    autoclose : true,
    startView : 'year',
    minView : 'year',
    todayBtn : true,
});

$(document).ready(refresh);
$("#order_search").click(refresh);

function refresh() {
    var id_work_order = $("#id_work_order").val();
    var now = new Date();
    var month = now.getMonth() + 1;
    var year = now.getFullYear();
    $("#querydate").attr("value", year + "-" + month);
    getTechPlan(month, year, id_work_order);
}

function getTechPlan(month, year, id_work_order) {
    Dajaxice.techdata.getTechPreparationPlan(getTechPlanCallBack, {
                                                "id_work_order" : id_work_order,
                                                "month" : month,
                                                "year" : year
    });
}

function getTechPlanCallBack(data) {
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

$(document).on("click", "#date_search", function(){
    var querydate = $("#querydate").val();
    var month = querydate.split("-")[1];
    var year = querydate.split("-")[0];
    var id_work_order = $("#id_work_order").val();
    getTechPlan(month, year, id_work_order);
});
