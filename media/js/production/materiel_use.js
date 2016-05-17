$(document).on("click", "#materieluse_search_form .btn", function() {
  Dajaxice.production.applyCardSearch(applyCardSearchCallBack, {"form": $("#materieluse_search_form").serialize()});
});

$(document).on("click","#workadd", function(){
  $(document).find("#id_order_index__contains").val("");
  Dajaxice.production.workorderSearch(workorderSearchCallBack, {"form": $("#workorder_search_form").serialize()});
});

function applyCardSearchCallBack(data){
  $("#table_div").html(data.html);
}
