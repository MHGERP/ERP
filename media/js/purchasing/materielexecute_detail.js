var materielChoice;
var detail_id_array = new Array();
var i = 0;
var materielExecuteId;

$('#submit-btn').click(function(){
    form = $("#detail_form");
    Dajaxice.purchasing.saveMaterielExecuteDetail(saveMaterielExecuteDetail_callback,
        {
          'form':$(form).serialize(true),
          'materielChoice' : materielChoice
        });
})

function saveMaterielExecuteDetail_callback(data){
    if (data.status == "1"){
      // $("#materielexecute_detail_table").html(data.detail_table);
      $("#materielexecute_detail_table tbody").after(data.detail_table);
      detail_id_array[i] = data.materielexecute_detail_id;
      i++;
      alert(data.message);
    }else{
      $("#detail_form").html(data.add_form);
    }
  
}

$(document).on("click","#add-btn",function(){
    document.getElementById("detail_form").reset();
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
  }
  alert(data.message);
}

$(document).on("click","#commit-btn",function(){
    Dajaxice.purchasing.materielExecuteCommit(materielExecuteCommit_callback, 
    {
      'detail_id_array' : detail_id_array,
      'materielChoice' : materielChoice,
      'materielExecuteId' : materielExecuteId
    });
});

function materielExecuteCommit_callback(data) {
  if(data.status == "1") {
    window.location.href = "/purchasing/materielExecute"
  }
  else {
    alert("error");
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
