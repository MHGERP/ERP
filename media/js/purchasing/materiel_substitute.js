$("#subapply_info_confirm").click(function(){
  var form= $("#subapply_info");
  subapply_id=$("#subapply_body").attyyr("subapplyid");
  Dajaxice.purchasing.UpdateSubapplyInfo(function(data){
      if(data.status==0){
          alert("保存成功！");
          window.location.reload();
      }
      else{
          alert("保存失败！");
      }
  },{
      'form':form.serialize(true),
      'subapply_id':subapply_id
  });
});

var sid;
$("#add_item").click(function(){
    sid=-1;
    Dajaxice.purchasing.getSubApplyItemForm(function(data){
        $("#subapply_item_form").html(data.html);
        $("#materiel_substitude_item_modal").modal();
    },{
        "sid":sid
    });
});
$(document).on("dblclick","tr[name='subapply_item']",function(){
    if($("#complete").size() == 0){
        return false;
    }
    sid = $(this).attr("sid");
    Dajaxice.purchasing.getSubApplyItemForm(function(data){
        $("#subapply_item_form").html(data.html);
        $("#materiel_substitude_item_modal").modal();
    },{
        "sid":sid
    });
});

$("#subapply_item_confirm").click(function(){
    Dajaxice.purchasing.UpdateSubapplyItem(function(data){
        if(data.status ==1 ){
            alert("表单提交失败,所有字段为必填字段");
        }
        else{
            window.location.reload();
        }
    },{
        'form':$("#subapply_item_form").serialize(true),
        'sid':sid,
        'subapplyid':$("#subapply_body").attr("subapplyid")
    });
});
$("#complete").click(function(){
    if(confirm("是否确认完成材料执行申请表填写?")){
        Dajaxice.purchasing.submitSubapply(function(data){
            window.location.reload();
        },{
            'subapplyid':$("#subapply_body").attr("subapplyid")
        });
    } 
});
$("#subapply_comment_confirm").click(function(){
  subapply_id=$("#subapply_body").attr("subapplyid");
  var usertitle=$("#comment_add").attr("usertitle");
  Dajaxice.purchasing.SubapplyComment(function(data){
      window.location.reload();
  },{
        "subapply_id":subapply_id,
        "usertitle":usertitle,
        "comment":$("#comment_area").val()
  });
    
});
