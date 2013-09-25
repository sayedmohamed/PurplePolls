/*
This file handles the ajax call of the user vote and the dynamic rendering of the results.
 */

$(document).ready(function() {
    $('#vote').click(create_vote);
});

var create_vote = function(e) {
    e.preventDefault()
    var value = $("form input[name='choice']:checked").val();
    var data = { choice: value };
    var args = { type:"POST", url:"/polls/" + jQuery.data(document.body, "poll_id") +"/vote/", data:data, complete:create_vote_complete };
    $.ajax(args);
};

var create_vote_complete = function(res, status) {
    if (status == "success") {
        $(".results").html(res.responseText);
    }
};
