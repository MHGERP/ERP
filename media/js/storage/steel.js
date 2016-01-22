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
    //var material_number_list = new Array();
	$(".refund-card-ensure-btn").click(function(){
        //$("tr.everyReturn").each(function(i){
        //    material_number_list.push($(this).attr("matnum"));
        //})
		//alert(material_number_list);

        var form_code = $("table").attr("fc");
        Dajaxice.storage.steelRefundEnsure(steelRefundEnsureCallBack, {'form_code':form_code});
	});
	$(".apply-card-ensure-btn").click(function(){
        var form_code =$("table").attr("iid");
        Dajaxice.storage.steelApplyEnsure(steelApplyEnsureCallBack,{'form_code':form_code});
	});
});

function steelRefundEnsureCallBack(data) {
    alert(data);
    window.location.reload();
}

function steelApplyEnsureCallBack(data){
    alert(data);
    window.location.reload();
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


function change_remark(itemid){
    mid = itemid;
    var a = $("tr#"+mid).find("td");
    $("#id_remark").val(a.eq(12).text());
/*    $("#id_storeRoonSelect").attr("disabled",true);*/
}

function save_remark(typeid){
	var remark = $("#id_remark").val();
	typeid = typeid;
/*	alert(typeid);
	alert(remark);
	alert(mid);*/
    Dajaxice.storage.saveRemark(save_remark_callback,{"remark":remark, "mid":mid, "typeid":typeid});
}

function save_remark_callback(data){
    if(data.flag){
    	$("#items_table").html(data.html);
        alert(data.message);
    }
    else{
        alert(data.message);
    }
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
