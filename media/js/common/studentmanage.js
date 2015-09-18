var glo_apply_id;
var glo_role_oper;
function get_subject_id(apply_id,role_oper){
  glo_apply_id = apply_id;
  glo_role_oper = role_oper;
}

function add_student() {
  $("#studentadd_error_message").empty();
  Dajaxice.common.AddStudent(add_student_callback,
                                {'form': $('#studentaddform').serialize(true),
                                 });
};

function add_student_callback(data){
    if(data.status == "2") {
    $.each(data.error_id, function (i, item){
      object = $('#'+item);
      object.css("border-color", 'red');
    });
  }
    $("#studentadd_error_message").append("<strong>"+data.message+"</strong>");
};

function search_student() {
  alert("search");
  Dajaxice.common.SearchStudent(search_student_callback,
                                {
                                 });
};


function change_overstatus(){
  var overstatus = $('#classchange_choice').find("option:selected").val();
  Dajaxice.common.change_apply_overstatus(change_overstatus_callback,{'apply_id':glo_apply_id,"changed_overstatus":overstatus,"change_role":glo_role_oper,});
}
function change_overstatus_callback(data){
  $("#div_changetable").html(data.table_fre);
}

function export_search () {
  Dajaxice.common.exportSearchStudents(export_search_students_callback,{'searchform':$('#studentsearchform').serialize(true)});
}

function export_search_students_callback(data){
  location.href = data.path;
}

$(document).on("click","#alloc_paginator .item_page",function(){
    page = $(this).attr("arg");
    Dajaxice.common.getSearchStudentPagination(getSearchStudentCallback,{"page":page,'searchform':$('#studentsearchform').serialize(true)});
});

function getSearchStudentCallback(data){
    $("#student_search").html(data.html);
}

