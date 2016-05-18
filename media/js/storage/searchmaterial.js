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
        var old_select_item = $("tr#select_item").attr("sid");
        if(select_item != null ||  old_select_item != null){
            if(select_item == null ){
                select_item = old_select_item;
            }
            Dajaxice.storage.searchMaterialApply(weldapply_callback,{"apply_form":$("#apply_form").serialize(),"select_item":select_item,"mid":mid,"apply_type":apply_type,"search_form":$("#search_material_form").serialize()});
        }
        else{
            alert("请选择领用材料")
        }
    })
    $(document).on("click","#search_material_btn",function(){
        apply_type = $("#search_material_btn").attr("apply_type");
        Dajaxice.storage.searchMaterial(search_material_callback,{"search_form":$("#search_material_form").serialize(),"apply_type":apply_type,"mid":mid});
    })
})

function applyitemrefresh_callback(data){
    $("#apply_form").html(data.form_html);
    refresh_select_item(data);
    $("#myModal").modal('show'); 
}

function refresh_select_item(data){
    $("#store_items_table").html(data.table_html);
    $("#show_select_item_div").html(data.show_html);
    var apply_store_thead = $("#apply_store_thead").html();
    var apply_select_item = $("#select_item").html();
    $("#show_select_item").append(apply_store_thead);
    $("#show_select_item").append(apply_select_item);
}

function weldapply_callback(data){
    $("#word_contain").html(data.word_html);
    $("#apply_form").html(data.form_html)
    if(data.show_select){
        refresh_select_item(data);
    }
    alert(data.message);   
}

function search_material_callback(data){
   $("#store_items_table").html(data.html); 
}
