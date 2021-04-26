$(window).on('load', function() {
    var win = $(this);
    if (win.width() < 801) {
  
      $('.asbcontent').removeClass('col-md-10');
      $('.asbcontent').addClass('w-100');

    } 
    else{
      $('.asbcontent').addClass('col-md-10');
      $('.asbcontent').removeClass('w-100');

    }
    if (win.width() < 1200) {
  
      $('#navitems').removeClass('col-10');
      $('#headernav').removeClass('col-2');
      $('#navitems').addClass('w-100');
      $("#searchinput" ).css( "width", "15rem" );
  
  
      } 
      else{
      $('#navitems').addClass('col-10');
      $('#headernav').addClass('col-2');
      $('#navitems').removeClass('w-100');
      $("#searchinput" ).css( "width", "25rem" );
  
      }
  
  });
    $(window).on('resize', function() {
    var win = $(this);
    if (win.width() < 801) {
  
      $('.asbcontent').removeClass('col-md-10');
      $('.asbcontent').addClass('w-100');

    } 
    else{
      $('.asbcontent').addClass('col-md-10');
      $('.asbcontent').removeClass('w-100');

    }
    if (win.width() < 1200) {
  
      $('#navitems').removeClass('col-10');
      $('#headernav').removeClass('col-2');
      $('#navitems').addClass('w-100');
      $("#searchinput" ).css( "width", "15rem" );
  
  
      } 
      else{
      $('#navitems').addClass('col-10');
      $('#headernav').addClass('col-2');
      $('#navitems').removeClass('w-100');
      $("#searchinput" ).css( "width", "25rem" );
  
      }
  
  });
  