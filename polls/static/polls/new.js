/*
This file handles the ajax call of the new poll creation and the dynamic rendering of the results.
 */

$(document).ready(function() {
    // Register the click actions
    $('#new').click(create_poll);
    $('#add_choice').click(add_choice);

    // Disable form submission until something changes
    $('input[type="text"]').keyup(function() {
        if($(this).val() != '') {
            $('input[type="submit"]').removeAttr('disabled');
        }
    });
});

choices = [];

// Async HTTP request to create a new poll on the server
create_poll = function (e) {
    e.preventDefault()
    $('input[type="submit"]').attr('disabled','disabled');

    // Make sure to add the new choice in case the user didn't click add
    if ($("form input[name='choice']:text").val().trim().length > 0) {
        add_choice(e);
    }

    // Make the ajax call
    var question = $("form input[name='question']:text").val();
    var data = { question: question, choices: choices.toString() };
    var args = { type: "POST", url: "/polls/new", data: data, complete: new_poll_complete };
    $.ajax(args);

    $('input[type="submit"]').removeAttr('disabled');
};

// Locally add a choice to a JSON array that is pushed when the user submits
add_choice = function(e) {
    e.preventDefault();
    var new_choice = $("form input[name='choice']:text").val();
    $("form input[name='choice']:text").val('').focus();
    $("#choices_list").append("<li>" + new_choice + "</li>");
    choices.push(new_choice);
};

// Callback from the Ajax query - display results / error msg
var new_poll_complete = function(res, status) {
    if (status === "success") {
        $(".poll_list_outer").html(res.responseText)
        var question = $("form input[name='question']:text").val();
        cleanup();
        popup_poll_added("You're poll '" + question + "' was added! ")
    }
    else {
        $(".message").html(res.responseText);
    }
};

// Clear out the form for a new poll entry
cleanup = function() {
    $("#choices_list").text('');
    $("form input[name='choice']:text").val('');
    $("form input[name='question']:text").val('');
};

// Popup message to let the user know a poll was added
popup_poll_added = function(msg) {
    var msg_div = $('<div class="popup"><p>' + msg + '</p></div>');
    $(".message").html((msg_div).fadeIn('slow').animate({opacity: 1.0}, 5000).fadeOut('slow',function() { msg_div.remove(); }));
};
