
$('#submit-btn').click(function(){
    form = $("#detail_form");
    var document_number_input = $("#document_number_input").val();
    var materiel_choice_select = $("#materiel_choice_select option:selected").attr("value");
    Dajaxice.purchasing.saveMaterielExecuteDetail(saveMaterielExecuteDetail_callback,
        {'form':$(form).serialize(true),
         'documentNumberInput' : document_number_input,
         'materielChoice' : materiel_choice_select
        });
})

function saveMaterielExecuteDetail_callback(data){
  if (data.status == "1"){
    // if success all field background turn into white
    // $(dispatch_div).html(data.table);
  }else{
  }
  alert(data.message);
  $("#add-detail-modal").modal('hide');
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
  $("#modal-body").html(data.add_form);
}