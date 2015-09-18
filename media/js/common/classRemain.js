$("#smallClassSelect").change(function(){
    var smallid = $(this).val();
  if (smallid != -1) Dajaxice.adminStaff.getSmallClass(getSmallClassCallBack, {"smallClassId": smallid,});
});

function getSmallClassCallBack(data){
    $("#smallClassTable").html(data);
};

$("#gradeSelect").change(function(){
    var grade = $(this).val();
  if (grade != -1) Dajaxice.teacher.getSmallClass(getSmallClassCallBack, {"grade": grade,});
});


$(document).on('click','#classRemainButton',function(){
  var smallid = $("#smallClassSelect").val();
  if (smallid != -1) {
    Dajaxice.adminStaff.updateSmallClass(updateSmallClassCallBack, {'form': $("#smallClass").serialize(true), "smallClassId": smallid});
    // $("#debug").text($("#smallClass").serialize());
  }
});

function updateSmallClassCallBack(data){
  $("#smallClassTable").html(data);
    alert("修改成功");
};

$(document).on('click','#classTeacherRemainButton',function(){
  var grade = $("#gradeSelect").val();
  if (grade != -1) {
    Dajaxice.teacher.updateSmallClass(updateSmallClassCallBack, {'form': $("#smallGradeClass").serialize(true), "grade": grade});
    // $("#debug").text($("#smallClass").serialize());
  }
});
