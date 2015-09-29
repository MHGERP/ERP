$(document).on("click", ".inventory_open", function(){
    var order_index = $(this).attr("args");
    var tem = $(this).parent().children().get(0);
    alert($(tem).val())
});
