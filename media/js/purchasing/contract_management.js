$(document).on("click", "table td a", function(){
  Dajaxice.purchasing.contractAmount(contractamount_callback,{'tid':$(this).attr("tid"), "bid":$(this).parent().parent().find("td:first").html(), "form":""});
})
$(document).on("click", "#contract_add_form #contract_submit", function(){
  form = $(this).parents("form");
  Dajaxice.purchasing.contractAmount(contractamount_callback,{'tid':$(this).attr("tid"), "bid":$(this).attr("bid"), "form":$(form).serialize(true)});
})
function contractamount_callback(data){

  if (data.status == "1"){
     $("#contract_div").html(data.table);
    $('#ContractManagementModal').modal('show');
  }else if(data.status == "2"){
    alert(data.message);
  }else if(data.status == "0"){
    alert(data.message);
    location.reload();
  }

}
