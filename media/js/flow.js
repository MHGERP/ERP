/**
 * @author tianwei
 * the whole flow style js
 */

/* Picture show flow*/
$(document).ready(function(){
  var $flow_container=$('#flow_container');

  $flow_container.imagesLoaded(function(){
    $flow_container.masonry({
      itemSelecter:'.box'
    });
  });
});
