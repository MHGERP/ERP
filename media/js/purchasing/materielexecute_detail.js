var materielChoice;
var i = 0;
var materielExecuteId;
$(function(){
    if($("#id_document_number").val()){
    $("#id_document_number").attr("disabled","disabled");
    $("#materiel_choice_select").attr("disabled","disabled");
    $("#add-btn").attr("disabled","disabled");
        
   // update_select();
    }
});
$('#submit-btn').click(function(){
    var selectedArray = Array();
    $("input.checkbox").each(function(){
        if(this.checked) selectedArray.push($(this).attr("args"));
    });
    Dajaxice.purchasing.saveMaterielExecuteDetail(saveMaterielExecuteDetail_callback,
        {
            'selected':selectedArray,
            "eid":$("#id_document_number").val()         
        });
});

function saveMaterielExecuteDetail_callback(data){
    //if (data.status == "1"){
      // $("#materielexecute_detail_table").html(data.detail_table);
     // $("#materielexecute_detail_table tbody").after(data.detail_table);
     // detail_id_array[i] = data.materielexecute_detail_id;
     // i++;
     // alert(data.message);
   // }else{
    //  $("#detail_form").html(data.add_form);
   // }
  alert(data.status);
  window.location.reload();

}

$(document).on("click","#add-btn",function(){
    var materiel_choice_select = $("#materiel_choice_select option:selected").attr("value");
    materielChoice = materiel_choice_select;
    form = $("#execute_form");
    Dajaxice.purchasing.saveMaterielExecute(saveMaterielExecute_callback, 
    {
      'form':$(form).serialize(true)
    });
});

function saveMaterielExecute_callback(data) {
  if(data.status == "1") {
    materielExecuteId = data.materielExecuteId;
    $("#id_document_number").attr("disabled","disabled");
    $("#materiel_choice_select").attr("disabled","disabled");
    $("#add-btn").attr("disabled","disabled");
  }
  alert(data.message);
}

$(document).on("click","#commit-btn",function(){
    Dajaxice.purchasing.materielExecuteCommit(materielExecuteCommit_callback, 
    {
      'materielExecuteId' : $("#id_document_number").val()
    });
});

function materielExecuteCommit_callback(data) {
    alert(data.message);
    if(data.status == "0") {
    window.location.href = "/purchasing/materielExecute";
  }
  
}
    
$("#materiel_choice_select").change(function(){
  var materiel_choice_select = $("#materiel_choice_select option:selected").attr("value");
  Dajaxice.purchasing.materielchoiceChange(choiceChange_callback, 
      {
        'materielChoice' : materiel_choice_select
      });
});

function choiceChange_callback(data) {
  $("#materielexecute_detail_table").html(data.materielexecute_detail_html);
  $("#myModalLabel").html(data.current_materiel_choice);
  $("#detail_select").html(data.select_materielexecute_html);
}


//selectall
$(document).on("click", "input#selectall", function(){
    var target = this.checked;
    $("input[type='checkbox']").each(function(){
        this.checked = target; 
    });
});

$(document).on("click","#detail_edit",function(){
  uid = $(this).attr("uid");
  Dajaxice.purchasing.GetMeterielExecuteForm(Detail_Edit_Callback,{'uid':uid});
});
function Detail_Edit_Callback(data){
  $('#materielexecute_modal').modal();
  $('#materielexecute_div').html(data.form);
}

$(document).on("click","#save_materiel_excecute",function(){
  Dajaxice.purchasing.materielExecuteInfo(MaterielExecuteInfo_Callback,{'form':$('#edit_materielexecute_form').serialize(true),'uid':uid})
});
function MaterielExecuteInfo_Callback(data){
  $('#materielexecute_modal').modal('hide');
  window.location.reload();
}

$("#save_tech_require").click(function(){
    var content=$("#tech_requirement_textarea").val();
    var execute_id=$("#id_document_number").val();
    Dajaxice.purchasing.saveExecuteTechRequire(function(data){
    $("#tech_requirement_content").val(content);
    },{
        "execute_id":execute_id,
        "content":content
    });
});

$("#tech_add").click(function(){
    $("#tech_requirement_textarea").val($("#tech_requirement_content").val());
});
