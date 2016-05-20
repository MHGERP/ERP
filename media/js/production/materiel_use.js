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

$(document).on("click","#materiel_use_table .btn", function(){
  tr = $(this).parent().parent();
  table = $("#materiel_use_add_div").find("table");
  table.append(tr);
  $(tr).find(".btn").text("删除").attr("class", "btn btn-danger");
});

$(document).on("click","#materiel_use_add_div .btn", function(){
  tr = $(this).parent().parent().remove();
});

$(document).on("click","#materieluse_add_type_form .btn", function(){
  iids = new Array();
  $("#materiel_use_add_div").find("tbody tr").each(function(){
    iids.push($(this).attr("iid"));
  });
  Dajaxice.production.createApplyCard(createApplyCardCallBack, {"form": $("#materieluse_add_type_form").serialize(), "iids":iids});
});

function createApplyCardCallBack(data){
  alert(data);
}

$(document).on("dblclick","#table_div table tr",function(){
  Dajaxice.production.getApplyCardDetail(getApplyCardDetailCallBack, {"aid": $(this).find("td:eq(0)").html()});
})

function getApplyCardDetailCallBack(data){
  $("#materiel_body_div").html(data);
  $("#materiel_add_model").modal("show");
}
