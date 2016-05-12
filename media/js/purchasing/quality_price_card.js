
$("#qualitycard_confirm").click(function(){
    var form=$("#quality_card_form");
    var quality_card_id=$("#quality_card_div").attr("qualitycardid");
    supplier_form_set=Array();
    supplier_id_set=Array();
    $(".supplierform").each(function(){
        supplier_form_set.push($(this).serialize(true));
        supplier_id_set.push($(this).attr("supplierselect"));
    });
    Dajaxice.purchasing.saveQualityCard(function(data){
        if(data.status ==0 ){
            window.location.reload();
        }
        else{
            alert("表单填写有误");
        }
    },{
        'form':$(form).serialize(true),
        'quality_card_id':quality_card_id,
        'supplier_form_set':supplier_form_set,
        'supplier_id_set':supplier_id_set
    });
});
$("#qualitycard_submit").click(function(){
    var quality_card_id=$("#quality_card_div").attr("qualitycardid");
      Dajaxice.purchasing.submitQualityCard(function(data){
    window.location.reload();
      },{'quality_card_id':quality_card_id});
});
$("#qualitycard_comment_confirm").click(function(){
    var quality_card_id=$("#quality_card_div").attr("qualitycardid");
    var usertitle=$("#comment_add").attr("usertitle");
    Dajaxice.purchasing.QualityCardComment(function(data){
        window.location.reload();
    },{
        "quality_card_id":quality_card_id,
        "usertitle":usertitle,
        "comment":$("#comment_area").val()
    });
});
