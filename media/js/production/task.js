function task_allocation_search(){
  Dajaxice.production.taskAllocationSearch(task_Allocation_callback,{"form":$("#search_form").serialize(),});
}

function task_Allocation_callback(data){
   $('#item_table').html(data.html); 
}

function task_allocation_remove(mid){
    Dajaxice.production.taskAllocationRemove(task_Allocation_remove_callback,{"form":$("#search_form").serialize(),"mid":mid})
}

function task_Allocation_remove_callback(data){
    $('#item_table').html(data.html);
}

function task_allocation_submit(mid){
    var id_string = mid.toString();
    var groupid = $('#table_select'+id_string).val()

    Dajaxice.production.taskAllocationSubmit(task_Allocation_submit_callback,{"form":$("#search_form").serialize(),"mid":mid,"groupid":groupid})
}

function task_Allocation_submit_callback(data){
    $('#item_table').html(data.html);
}

function task_confirm_search(){
    Dajaxice.production.taskConfirmSearch(task_Confirm_callback,{"form":$("#search_form").serialize(),});
}

function task_Confirm_callback(data){
    $('#item_table').html(data.html);
}

function task_confirm_finish(mid){
    Dajaxice.production.taskConfirmFinish(task_Confirm_finish_callback,{"form":$("#search_form").serialize(),"mid":mid})
}

function task_Confirm_finish_callback(data){
    $('#item_table').html(data.html);
}

function task_confirm_view(mid){
    Dajaxice.production.taskConfirmView(task_Confirm_view_callback,{"mid":mid})
}

function task_Confirm_view_callback(data){
    $('#task_view_modal').modal('show');
    $('#task_plan_table').html(data.html);
    var btn = document.getElementById('task_check_button');
    btn.style.visibility = "hidden"; 

}

function task_plan_search(){
    Dajaxice.production.taskPlanSearch(task_plan_search_callback,{"form":$("#search_form").serialize()});
}

function task_plan_search_callback(data){
    $('#item_table').html(data.html);
}

function task_plan_change(mid){
    Dajaxice.production.taskPlanChange(task_plan_change_callback,{"mid":mid});
}

function task_plan_change_callback(data){
    $('#task_plan_modal').modal('show');
    $('#task_plan_table').html(data.html);
    $('#id_startdate').datetimepicker({
        format:'yyyy-mm-dd',
        minView: 2,
        autoclose: true,
    });
    $('#id_enddate').datetimepicker({
        format:'yyyy-mm-dd',
        minView: 2,
        autoclose: true,
    });
}


function task_plan_submit(){
    mid = $('#task_plantime_table').attr("value");
   startdate = $('#id_startdate').attr("value");
   enddate = $('#id_enddate').attr("value");
   if(startdate =="" | enddate == "")
   {
        alert("日期不能为空！");
        return ; 
   }
   Dajaxice.production.taskPlanSubmit(task_plan_submit_callback,{"form":$("#search_form").serialize(),"mid":mid,"startdate":startdate,"enddate":enddate});
}

function task_plan_submit_callback(data){
    $('#task_plan_modal').modal('hide');
    alert("修改成功");
    $('#item_table').html(data.html);
}

function task_confirm_check(mid){
 Dajaxice.production.taskConfirmView(task_Confirm_check_callback,{"mid":mid})
}

function task_Confirm_check_callback(data){
    $('#task_view_modal').modal('show');
    $('#task_plan_table').html(data.html);
    var btn = document.getElementById('task_check_button');
    btn.style.visibility = "visible"
    $('#td_check_content').html('<textarea style="width:98%; height:200px;" id="input_check_content" type="text" >在此处输入检查内容：</textarea>');
}

function task_check(){
    mid = $('#task_view_table').attr('value');
    check_content = $('#input_check_content').attr('value'); 
    Dajaxice.production.taskCheck(task_check_callback,{"mid":mid,"check_content":check_content});
}

function task_check_callback(data){
    $('#task_plan_table').html(data.html);
    var btn = document.getElementById('task_check_button');
    btn.style.visibility = "hidden"; 
}
