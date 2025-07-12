$(document).ready(function () {
    $('#upload-csv').on('click', function () {
      const fileInput = $('input[type="file"]')[0];

      if (!fileInput.files.length) {
        e.preventDefault();
      }
      $('.container').hide();
      $('.loader-div').fadeIn();
    });

    $('.collapsible-toggle').click(function () {
      $(this).toggleClass('active');
      $(this).next('.collapsible-content').slideToggle();
    });

    $('#load-data').on('click',function(e){
      window.location.href = '/stored-data';
    })
});
