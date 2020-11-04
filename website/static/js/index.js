$(function() {
    $('#sendButton').on('click', function() {
      var message = document.getElementById('messageSend').value;
      console.log(message);
      $.getJSON('/run_messageSender', {val:message},
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

fetch('/get_messages').then(function(response){
  return response.text();
}).then(function(text){
  console.log("GET response text:");
  console.log(text);
})