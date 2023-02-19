$(document).ready(function () {
  
  // to tooltips style
  $(function () {
    $('[data-bs-toggle="tooltip"]').tooltip()
  });


  /* The menu sidebar */
  var width = $(window).width();

    if (width < 992)
    {
      $(".menu-icon").on("click", function () {
        $(".menu-icon").addClass("d-none")
        $(".small-icon").removeClass("d-none")
        $(".sidebar").removeClass("d-none")
      });
      $(".small-icon").on("click", function () {
        $(".small-icon").addClass("d-none")
        $(".menu-icon").removeClass("d-none")
        $(".sidebar").addClass("d-none")
      });
    }


});