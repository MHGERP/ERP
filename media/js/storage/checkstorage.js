$(document).ready(function(){
    $("div#search_form").on("click","#check_btn",function(){
        Dajaxice.storage.searchMateriel(search_materiel_callback,{"form":$("form#search_form").serialize()})
    });
    function search_materiel_callback(data){
        $("div#materiel_table").html(data.html);
    }
    $("div#search_form").on("change","#db_type",function(){
        var db_type = $("#db_type").val();
        Dajaxice.storage.changeStorageDb(change_db_callback,{'db_type':db_type,'form':$('form#search_form').serialize()});
    });
    function change_db_callback(data){
        $("div#search_form").html(data.form_html);
        $("div#materiel_table").html(data.table_html);
        $("#materiel_type").select2();
    }
    $("#confirm_btn").on("click",function(){
        var selected = $("input[name='check_radio']:checked").attr("iid");
        Dajaxice.storage.chooseStorageMateriel(choosemateriel_callback,{"form":$('form#search_form').serialize(),"selected":selected})
    })
    function choosemateriel_callback(data){
    }
})
