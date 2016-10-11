$(function() {


    // Submit post on submit
    $('#post-form').on('submit', function(event) {
        event.preventDefault();
        console.log("form submitted!") // sanity check
        if ($("[name=crypt]").val() != null)
            create_post($("[name=crypt]").val());
    });

    // Submit decrypt-post on submit
    $('#decrypt-form').on('submit', function(event) {
        event.preventDefault();
        console.log("form submitted!") // sanity check
        if ($("[name=crypt]").val() != null)
            decrypt_post($("[name=crypt]").val());
    });

    // AJAX for posting
    function create_post(type) {
        console.log("create post is working!") // sanity check
        $.ajax({
            url: "create_post/" + parseInt(type) + "/", // the endpoint
            type: "POST", // http method
            data: { the_post: $('#id_post-text').val() }, // data sent with the post request
            beforeSend: function(xhr, settings) {
                //call global beforeSend func
                $.ajaxSettings.beforeSend(xhr, settings);

            },
            // handle a successful response
            success: function(json) {
                //$('#id_post-text').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                var name = "<b>Ключ: </b>"
                if (type == 2) {
                    name = "<b>Открытый ключ: </b>"
                }
                var span = "<p class='key' id='key_span'style='display: none'>" + name + json.key + "</p>";
                $('#id_decrypt-text').val(json.crypted_text);
                if ($('#key_field').children().length != 0) {
                    $('#key_field').children()[0].remove()
                }

                $('#key_field').prepend(span);
                $('#key_span').fadeIn(200);


                console.log("success"); // another sanity check
                // $(btn).css('background-color','white');
            },
            // handle a non-successful response
            error: function(xhr, errmsg, err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

    // AJAX for posting
    function decrypt_post(type) {
        console.log("decrypt post is working!") // sanity check
        $.ajax({
            url: "decrypt_post/" + parseInt(type) + "/", // the endpoint
            type: "POST", // http method
            data: { the_post: $('#id_decrypt-text').val() },
            // handle a successful response
            success: function(json) {
                $('#id_decrypt-text').val(''); // remove the value from the input
                $('#id_decrypt-text').val(json.text);
                if (json.text == '') {
                    $('#id_decrypt-text').val($('#id_post-text').val());
                }
                console.log("private key: " + json.privkey);
                console.log("success"); // another sanity check
            },
            // handle a non-successful response
            error: function(xhr, errmsg, err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});
