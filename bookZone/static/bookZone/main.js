$(document).ready(function(){
  
  
  //------------------------------------//
  //Wow Animation//
  //------------------------------------// 
  wow = new WOW(
        {
          boxClass:     'wow',      // animated element css class (default is wow)
          animateClass: 'animated', // animation css class (default is animated)
          offset:       0,          // distance to the element when triggering the animation (default is 0)
          mobile:       false        // trigger animations on mobile devices (true is default)
        }
      );
      wow.init();


$(".rating input").change(function(e){
  var rate = $(this).val();
  var id = $('#id').val()
  $(location).attr('href',"rate/"+id+"/"+rate)
})

$('.rating input').ready(function() {
  var rateVal = $('#rate').val();
  $('input[value=' + rateVal + ']').prop('checked', true);

})

$("#saveChanges").click(function () {
    var username = $('#username').val()
    var firstname = $('#firstname').val()
    var lastname = $('#lastname').val()
    var email = $('#email').val()

      $.ajax({
        url: 'save',
        data: {
          'username': username,
          'firstname': firstname,
          'lastname': lastname,
          'email' : email
        },
        success: function (d) {
          window.location = d
        }
      });

    });

});

