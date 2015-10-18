
$('#submit-btn').click(function(){
    form = $("#detail_form");
    var document_number_input = $("#document_number_input").val();
    var materiel_choice_select = $("#materiel_choice_select option:selected").attr("value");
    if(document_number_input == null || document_number_input == "") {
      alert("请输入单据编号！");
      return;
    }
    Dajaxice.purchasing.saveMaterielExecuteDetail(saveMaterielExecuteDetail_callback,
        {'form':$(form).serialize(true),
         'documentNumberInput' : document_number_input,
         'materielChoice' : materiel_choice_select
        });
})

function saveMaterielExecuteDetail_callback(data){
  if (data.status == "1"){
    alert(data.message);
    // $("#errorsFieldDiv").html("");
    $("#add-detail-modal").modal('hide');
    window.reload();
  }else{
    // alert(data.errors.Html());
    // alert(data.add_form);
    $("#detail_form").html(data.add_form);
    // $("#errorsFieldDiv").html(data.errors);
  }
  
}


$("#materiel_choice_select").change(function(){
  var materiel_choice_select = $("#materiel_choice_select option:selected").attr("value");
  // alert(materiel_choice_select);
  Dajaxice.purchasing.materielchoiceChange(choiceChange_callback, 
      {
        'materielChoice' : materiel_choice_select
      });
})

function choiceChange_callback(data) {
  $("#materielexecute_detail_table").html(data.materielexecute_detail_html);
  $("#myModalLabel").html(data.current_materiel_choice);
  $("#detail_form").html(data.add_form);
}
