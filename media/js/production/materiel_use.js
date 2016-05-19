$(document).on("click", "#materieluse_search_form .btn", function() {
  Dajaxice.production.applyCardSearch(applyCardSearchCallBack, {"form": $("#materieluse_search_form").serialize()});
});

$(document).on("click","#materieluse_add_search_form .btn", function(){
  Dajaxice.production.materialuseSearch(materialuseSearchCallBack, {"form": $("#materieluse_add_search_form").serialize()});
});

function applyCardSearchCallBack(data){
  $("#table_div").html(data.html);
}

function materialuseSearchCallBack(data){
  $("#materiel_use_table").html(data.html);
}
