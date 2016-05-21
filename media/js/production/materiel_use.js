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

var apply_code, tr_type, mid;
$(document).on("dblclick","#materiel_body_div table tr", function(){
  if(typeof($(this).attr("name")) != "undefined"){
    apply_code = $("#materiel_body_div").find("#aid_code").attr("aid_code");
    tr_type = $(this).attr("name");
    mid = $(this).attr("mid");
    Dajaxice.production.getApplyCardForm(getApplyCardFormCallBack, {"aid":apply_code, "tr_type":tr_type, "mid":mid});
  }
})

function getApplyCardFormCallBack(data){
  $("#materiel_add_model").modal("hide");
  $("#materiel_modify_body_div").html(data);
  $("#materiel_modify_model").modal("show");
}

$(document).on("click","#materiel_modify_model #submit", function(){
  Dajaxice.production.saveApplyCardForm(saveApplyCardFormCallBack, {"form":$("#materiel_modify_form").serialize(), "aid":apply_code, "tr_type":tr_type, "mid":mid});
})

function saveApplyCardFormCallBack(data){
  if(data.status ==1){
    alert("保存成功");
    $("#materiel_modify_model").modal("hide");
    Dajaxice.production.getApplyCardDetail(getApplyCardDetailCallBack, {"aid": apply_code});
  }

}

$(document).on("click","#materiel_body_div span[role='auditor'], #materiel_body_div span[role='applicant'], #materiel_body_div span[role='inspector']", function(){
  apply_code = $("#materiel_body_div").find("#aid_code").attr("aid_code");
  Dajaxice.production.confirmApplyCardForm(confirmApplyCardFormCallBack, {"aid":apply_code, "role":$(this).attr("role")});
})

function confirmApplyCardFormCallBack(data){
  alert(data.message);
  if(data.status ==1){
    Dajaxice.production.getApplyCardDetail(getApplyCardDetailCallBack, {"aid": apply_code});
  }
}
