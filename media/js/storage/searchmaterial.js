var mid;
var apply_type;
$(document).ready(function(){
    $(document).on("dblclick","tr[name='apply_item_tr']",function(){
        mid = $(this).attr("mid");
        apply_type = $("#search_material_btn").attr("apply_type");
        Dajaxice.storage.applyItemRefresh(applyitemrefresh_callback,{"mid":mid,"apply_type":apply_type});
    })
    $(document).on("click","#apply_item_save",function(){
        var select_item = $("input[name='radio_item']:checked").val();
        if(select_item != null){
            Dajaxice.storage.searchMaterialApply(weldapply_callback,{"apply_form":$("#apply_form").serialize(),"select_item":select_item,"mid":mid,"apply_type":apply_type});
        }
        else{
            alert("请选择领用材料")
        }
    })
    $(document).on("click","#search_material_btn",function(){
        Dajaxice.storage.searchMaterial(search_material_callback,{"search_form":$("#search_material_form").serialize(),"apply_type":apply_type});
    })
})

function applyitemrefresh_callback(data){
    $("#apply_form").html(data.form_html);
    $("#store_items_table").html(data.table_html);
    $("#show_select_item_div").html(data.show_html);
    var apply_store_thead = $("#apply_store_thead").html();
    var apply_select_item = $("#select_item").html();
    $("#show_select_item").append(apply_store_thead);
    $("#show_select_item").append(apply_select_item);
    $("#myModal").modal('show'); 
}

function weldapply_callback(data){
     if(data.flag){
        $("#word_contain").html(data.html);
        $("#myModal").modal("hide");
    }
    alert(data.message);   
}

function search_material_callback(data){
   $("#store_items_table").html(data.html); 
}
