var mid;
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
    $(document).on("dblclick","tr[name='item_tr']",function(){
        mid = $(this).attr("id");
        $("#myModal").modal('show');
    })
    $(document).on("click","#steel_entry_modify",function(){
        Dajaxice.storage.saveSteelEntryStoreRoom(save_storeRoom_callback,{
            "form":$("#entry_item_form").serialize(),
            "mid":mid,
        });
    })
    $(document).on("dblclick","tr[name='remark_tr']",function(){
        $("#entryRemarkModal").modal('show');
    })
    $(document).on("click","#steel_entry_remark",function(){
        Dajaxice.storage.saveSteelEntryRemark(save_remark_callback,{
            "form":$("#entry_remark_form").serialize(),
            "eid":$("div#steelentry_items").attr('eid'),
        });
    })
    $(document).on("click","span[name='steel_entry_confirm']",function(){
        alert("aa")
        Dajaxice.storage.steelEntryConfirm(steel_entry_confirm_callback,{"eid":$("div#steelentry_items").attr('eid'),"role":$(this).attr("role")})
    })
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

var mid;
function change_remark_storeRoom(itemid){
    mid = itemid;
    var a = $("tr#"+mid).find("td");
    $("#id_remark").val(a.eq(12).text());
}

function save_storeRoom_callback(data){
    $("#items_table").html(data.html);
    alert(data.message);
}
function save_remark_callback(data){
    $("div#steelentry").html(data.html);
    alert(data.message);
}
$(document).ready(function(){
	if($("#entry_item_form").attr("iid")=="False"){
		$("#id_store_room").attr("disabled","disabled");
	};
});

function steel_entry_confirm_callback(data){
    $("div#steelentry").html(data.html);
    alert(data.message);
}
