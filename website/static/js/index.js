$(function() {
    $('#sendButton').on('click', function() {
      var message = document.getElementById('messageSend').value;
      console.log(message);
      $.getJSON('/run', {val:message},
      function(data) {
      
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