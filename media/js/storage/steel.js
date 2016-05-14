var mid;
$(document).ready(function(){
	$(".apply-card-search-btn").click(function(){
		form=$(".apply-card-search-form").serialize(true);
		Dajaxice.storage.searchApplyCard(searchApplyCard_CallBack,{'form':form});
	});
	$(".refund-card-search-btn").click(function(){
		form=$(".refund-card-search-form").serialize(true);
		Dajaxice.storage.searchSteelRefundCard(searchRefundCard_CallBack,{'form':form});
	});
	$(".ledger-search-btn").click(function(){
		form=$(".ledger-search-form").serialize(true);
		Dajaxice.storage.searchSteelLedger(searchSteelLedger_CallBack,{'form':form});
	});
	$(".refund-card-ensure-btn").click(function(){
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
        Dajaxice.storage.steelEntryConfirm(steel_entry_confirm_callback,{"eid":$("div#steelentry_items").attr('eid'),"role":$(this).attr("role")})
    })
    $(document).on("dblclick","tr[name='apply_item_tr']",function(){
        mid = $(this).attr("id");
        $("#myModal").modal('show');
    })
    $(document).on("click","#search_material_btn",function(){
        Dajaxice.storage.searchMaterial(search_material_callback,{"search_form":$("#search_material_form").serialize(),"search_type":"steel",});
    })
    $(document).on("click","#steel_select_save",function(){
        var select_item = $("input[type='radio']:checked").val();
        if(select_item != null){
            Dajaxice.storage.steelMaterialApply(steelapply_callback,{"select_item":select_item,"mid":mid});
        }
        else{
            alert("请选择领用材料");
        }
    })
    $(document).on("click","span[name='steel_applycard']",function(){
        var role = $(this).attr('role');
        var aid = $("div#steelapplycard_table").attr('aid');
        if(confirm("领用单确认后不能再修改")){
            Dajaxice.storage.steelApplyCardConfirm(steel_applycard_confirm_callback,{"aid":aid,"role":role});
        }
    })
    $(document).on("click","span[name='steel_refund']",function(){
        var role = $(this).attr('role');
        var rid = $("#refund_table").attr("rid");
        if(confirm("退库单确认后不能再次修改")){
            Dajaxice.storage.steelRefundConfirm(steel_refund_callback,{"rid":rid});
        }
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
function search_material_callback(data){
   $("#store_items_table").html(data.html); 
}
function steelapply_callback(data){
    if(data.flag){
        $("#myModal").modal('hide');
        $("#steelapplycard").html(data.html);
    }
    alert(data.message);
}
function steel_applycard_confirm_callback(data){
    $("div#steelapplycard").html(data.html);
    alert(data.message);
}
function steel_refund_callback(data){
    $("div#refund_table_div").html(data.html);
    alert(data.message);
}
