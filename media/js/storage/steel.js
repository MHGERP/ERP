$(document).ready(function(){
	$(".apply-card-search-btn").click(function(){
		form=$(".apply-card-search-form").serialize(true);
		Dajaxice.storage.searchApplyCard(searchApplyCard_CallBack,{'form':form});
	});
	$(".refund-card-search-btn").click(function(){
		form=$(".refund-card-search-form").serialize(true);
		Dajaxice.storage.searchRefundCard(searchRefundCard_CallBack,{'form':form});
	});
	$(".ledger-search-btn").click(function(){
		form=$(".ledger-search-form").serialize(true);
		Dajaxice.storage.searchSteelLedger(searchSteelLedger_CallBack,{'form':form});
	});
	$(".refund-card-ensure-btn").click(function(){
		alert("退库成功");
	});
	$(".apply-card-ensure-btn").click(function(){
        var form_code =$("table").attr("iid");
        Dajaxice.storage.steelApplyEnsure(steelApplyEnsureCallBack,{'form_code':form_code});
	});
});

function steelApplyEnsureCallBack(data){
    
}

function searchSteelLedger_CallBack(data){
	if(data["message"]=="error"){
		alert("form error");
	}
	if(data["message"]=="success"){
		$(".steel-ledger-table").html(data["result_table"]);
	}
}

function searchApplyCard_CallBack(data){
	if(data["message"]=="error"){
		alert("form error");
	}
	if(data["message"]=="success"){
		$(".apply-cards-table").html(data["result_table"]);
	}
}

function searchRefundCard_CallBack(data){
	if(data["message"]=="error"){
		alert("form error");
	}
	if(data["message"]=="success"){
		$(".refund-cards-table").html(data["result_table"]);
	}
}


function change_steelEntryItem(itemid){
    mid = itemid;
    var a = $("tr#"+mid).find("td");
    $("input#id_remark").val(a.eq(8).text());
}

function save_steel_entry_item(){
     Dajaxice.storage.steelEntryItemSave(save_steel_entry_item_callback,{"form":$("#entry_item_form").serialize(),"mid":mid});
}

function save_steel_entry_item_callback(data){
    if(data.flag){
        alert(data.message);
    }
    else{
        alert(data.message);
    }
    location.reload();
}

function steel_entry_confirm(eid){
    var entry_code = $("#input_entry_code").val();
    Dajaxice.storage.steelEntryConfirm(steel_entry_confirm_callback,{"eid":eid,"entry_code":entry_code}); 
}

function steel_entry_confirm_callback(data){
    if(data.flag){
        alert("入库单确认成功");
        window.location.reload();
    }
    else{
        alert("入库单确认失败");
    }
}
