var modals=$(".modal");
var height=$(window).height();
var width=$(window).width();
modals.each(function(){
    var pos=$(this).position();
    if(typeof($(this).attr("modal-size"))!="undefined"){
        size=$(this).attr("modal-size")*1;
        $(this).height(height*size);
        $(this).width(width*size);
        var tp=height*(1-size)/2;
        var lt=width*(1-size)/2;
        $(this).css({"top":tp+250,"left":lt+280});
    }
    else if(typeof($(this).attr("modal-size-width"))!="undefined"){
        size=$(this).attr("modal-size-width")*1;
        $(this).width(width*size);
        var lt=width*(1-size)/2;
        $(this).css({"left":lt+280});
    }
});
