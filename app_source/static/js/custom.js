

    $(function () {
// setTimeout() function will be fired after page is loaded
// it will wait for 5 sec. and then will fire
// $(".message_flash").hide() function
        setTimeout(function () {
            $(".message_flash").hide('blind', {}, 500)
        }, 5000);
    })

    $(document).ready(function () {
        $('#dtBasicExample').DataTable({
            "pagingType": "simple" // "simple" option for 'Previous' and 'Next' buttons only
        });
        $('.dataTables_length').addClass('bs-select');
    });


    $(document).ready(function () {
        $('#data').after('<div id="nav"></div>');

        var rowsShown = 7;
        var rowsTotal = $('#data tbody tr').length;
        var numPages = rowsTotal / rowsShown;
        $('#nav').append('Page : ');
        for (i = 0; i < numPages; i++) {
            var pageNum = i + 1;
            $('#nav').append('<a href="#" rel="' + i + '">' + pageNum + '</a> ');
        }


        $('#data tbody tr').hide();
        $('#data tbody tr').slice(0, rowsShown).show();

        $('#nav a:first').addClass('active');

        $('#nav a').bind('click', function () {

            $('#nav a').removeClass('active');
            $(this).addClass('active');
            var currPage = $(this).attr('rel');
            var startItem = currPage * rowsShown;
            var endItem = startItem + rowsShown;
            $('#data tbody tr').css('opacity', '0.0').hide().slice(startItem, endItem).css('display', 'table-row').animate({opacity: 1}, 300);
        });
    });

  $(function () {

    // MENU
    $('.nav-link').on('click',function(){
      $(".navbar-collapse").collapse('hide');
    });


    // AOS ANIMATION
    AOS.init({
      disable: 'mobile',
      duration: 800,
      anchorPlacement: 'center-bottom'
    });


    // SMOOTH SCROLL
    $(function() {
      $('.nav-link').on('click', function(event) {
        var $anchor = $(this);
          $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top - 0
          }, 1000);
            event.preventDefault();
      });
    });  


    // PROJECT SLIDE
    $('#project-slide').owlCarousel({
      loop: true,
      center: true,
      autoplayHoverPause: false,
      autoplay: true,
      margin: 30,
      responsiveClass:true,
      responsive:{
          0:{
              items:1,
          },
          768:{
              items:2,
          }
      }
    });

  });


    

