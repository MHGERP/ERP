$(document).ready(refresh);

function refresh() {
    alert(window.location.href);
}

alert("cao");
/*$("#id_save").click(function(){
    Dajaxice.techdata.saveWeldJointIndex(
        function(data) {
            alert($("#index_input").val());
            if(data == "ok")
                alert("保存成功");
            else
                alert("保存失败");
        },
        {
            "iid" : 
            "index" : $("#index_input").val();
        }
    );
   alert("cnm");
});*/
$(document).on("click", "#id_save", function() {
    //alert("cap");
    
});
