var uid=0;
function refreshMutilipSelect(){
  var build = function(select, tr) {
    select.multiselect();
    return false;
  }($('#id_course_to_class'));
  var build = function(select, tr) {
    select.multiselect();
    return false;
  }($('#id_class_week'));
  var build = function(select, tr) {
    select.multiselect();
    return false;
  }($('#id_class_time'));
}
$(document).ready(function() {
  refreshMutilipSelect();
});


$('#course_info_modal #save_course').click(function(){
  page = $(".course_paginator").find(".disabled").attr("value");
  Dajaxice.adminStaff.CourseInfo(Course_callback,{'form':$("#course_form").serialize(true),'uid':uid,'page':page})
})
// $('#course_importdata_modal #save').click(function(){
//   page = $(".course_paginator").find(".disabled").attr("value");
//   Dajaxice.adminStaff.CourseImportData(Course_callback,{'form':$("#course_importdata_form").serialize(true),'page':page})
// })

$(document).on("click","table td",function(){
  uid=$(this).parent().find("button").attr("uid");
  if($(this).find("button").length >0){
    page = $(".course_paginator").find(".disabled").attr("value");
    Dajaxice.adminStaff.DeleteCourse(Course_callback,{'uid':uid,'page':page});
  }else{
    Dajaxice.adminStaff.GetCourseForm(CourseForm_callback,{'uid':uid});
  }
})

function Course_callback(data){
  if(data.status=='1'){
    $("#course_section").html(data.table);
    $("#course_info_modal").modal('hide');
    $('#course_form_div').html(data.form);
    refreshMutilipSelect();
    uid=0;
  }else if(data.status =='0'){
    $('#course_form_div').html(data.form);
    refreshMutilipSelect();
  }else if(data.status=='2'){
    $("#course_section").html(data.table);
  }
  if(data.message.length() !=0){
    alert(data.message);
  }
}

function CourseForm_callback(data){
  $('#course_form_div').html(data.form);
  refreshMutilipSelect();
  $("#course_info_modal").modal('show');
}
$(document).on("click",".course_paginator .item_page",function(){
      page = $(this).attr("arg");
      Dajaxice.adminStaff.CoursePagination(Course_callback,{'page':page});
})

$("#exportCourse").on("click",function(){
  Dajaxice.adminStaff.exportSearchCourse(export_search_course_callback,{});
})

function export_search_course_callback(data){
  location.href = data.path;
}

var options={
  url:"/adminStaff/importCourseData",
  clearForm:true,
  resetForm:true,
  error:function(data){
  },
  success:function(data){
    if(data.status=='0'){
      location.href = data.path;
    }else if(data.status=='1'){
      $("#course_section").html(data.table);
    }
    alert(data.message);
    $("#course_importdata_modal").modal('hide');
  },
  };
$('#course_importdata_form').submit(function(){
  $('#course_importdata_form').ajaxSubmit(options);
  return false;
})
