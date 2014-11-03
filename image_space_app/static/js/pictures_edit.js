$(document).ready(function(){
  Caman("#edit_image", function(){
    this.render();
  });
  
  $(document).on('change', '#brightness', function(e) {
    var brightness = $("#brightness").val();
    $("#brightness_count").text(brightness);
   
    Caman("#edit_image", function(){
      this.reset()
      this.brightness(brightness).render();
    });
  });
});