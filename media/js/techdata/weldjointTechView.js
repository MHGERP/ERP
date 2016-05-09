$(document).ready(refresh);

var id_work_order;

function refresh() {
    var url = window.location.href;
    var arr = url.split("/");
    id_work_order = arr[arr.length - 2];
}

$("#id_save").click(function(){
    var index = $("#index_input").val();
    Dajaxice.techdata.saveWeldJointIndex(
        function(data) {
            if(data == "ok")
                alert("保存成功");
            else
                alert("保存失败");
        },
        {
            "id_work_order" : id_work_order,
            "index" : index,
        }
    );
});

var cell;
$(document).on("click", ".btn-danger", function() {
    cell = this;
    var uid = $(cell).attr("uid");
    if(confirm("确定删除吗？")){
        Dajaxice.techdata.deleteWeldJointDetail(
            function(data) {
                var row = $(cell).parent().parent();
                var row_next = row.next();
                row.remove();
                row_next.remove();
            },
            {
                "uid" : uid
            }
        )
    }
});
