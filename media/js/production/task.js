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
    $('#task_view_table').html(data.html);
}
