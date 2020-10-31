$(function() {
    $('#sendButton').on('click', function(e) {
      e.preventDefault()
      $.getJSON('/run', {value},
      function(data) {
          //value = document.getElementById("message").value
      });
      return false;
    });
  });

function validate(name){
    if(name.length < 2 || name.length > 20){
        return false
    }
    return true;
}