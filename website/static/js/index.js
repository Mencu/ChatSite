$(function() {
    $('#sendButton').bind('click', function() {
      var value = document.getElementById('messageSend').value
      $.getJSON('/run_messageSender', 
        {val:value},
        function(data) {
      
        });
    });
});

// $('.container').infiniteScroll({
//     // options
//     path: '.pagination__next',
//     append: '.post',
//     history: false,
//   });

window.addEventListener("load", function(){
    var update_loop = setInterval(update, 100);
    update()
});

function update() {

    fetch('/get_messages')
        .then(function (response) {
            return response.text();
        }).then(function (text) {
            console.log("GET response text:");
            console.log(text);
        });
}
