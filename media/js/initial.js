$(document).ready(function(){
    $("[select2='true']").each(function(){
        $(this).select2();
    });
    $("[date_picker = 'true']").each(function(){
        $(this).datetimepicker({format:"yyyy-mm-dd",minView:2,autoclose:true});
    })
})
