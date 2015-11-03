var modals=$(".modal");
var height=$(window).height();
var width=$(window).width();
modals.each(function(){
    var pos=$(this).position();
    if(typeof($(this).attr("modal-size"))!="undefined"){
        size=$(this).attr("modal-size")*1;
        alert(size);
        $(this).height(height*size);
        $(this).width(width*size);
        var tp=height*(1-size)/2;
        var lt=width*(1-size)/2;
        $(this).css({"top":tp+250,"left":lt+280});
    }
});
