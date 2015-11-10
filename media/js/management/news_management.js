$("#id_news_cate").change(refresh);

function refresh() {
    var news_cate = $("#id_news_cate").val();
    Dajaxice.management.getNewsList(getNewsCallBack, {"news_cate": news_cate});
}
function getNewsCallBack(data) {
    $("#widget-content").html(data.html);
    turn_page();
}

$(document).on("click", ".btn-delete", function() {
    news_id = $(this).parent().parent().attr("iid");
    if(confirm("你确定删除该头衔？")) {
        Dajaxice.management.deleteNews(refresh, {"news_id": news_id});
    }
});



function turn_page() {
	var ids = ["#news-next-page", "#news-previous-page"];
	var news_cate = $("#id_news_cate").val();
	for(var tagid in ids) {
		tagid = ids[tagid];
		// alert(tagid);
		$(tagid).attr('onclick',
					  "Dajaxice.management.getNewsList(getNewsCallBack, { "
					  + "'news_cate' : '" + news_cate + "',"
					  +	"'news_page' : '" + $(tagid).attr("arg") + "'"
					  + "});return false;");
	};
};

window.onload = function() {
	turn_page();
}