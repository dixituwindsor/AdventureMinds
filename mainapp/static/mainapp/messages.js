let input_message = $('#input-message');
let message_body = $('.msg_card_body');
let send_message_form = $('#send-message-form');
const USER_ID = $('#logged-in-user').val();

let loc = window.location;
let wsStart = 'ws://';

if(loc.protocol === 'https') {
    wsStart = 'wss://';
}
let endpoint = wsStart + loc.host + loc.pathname;

var socket = new WebSocket(endpoint);

socket.onopen = async function(e) {
    console.log('WebSocket connection opened', e);
    send_message_form.on('submit', function (e) {
        e.preventDefault();
        let message = input_message.val();
        let receiver_id = get_active_other_user_id();
        let thread_id = get_active_thread_id();

        let data = {
            'message': message,
            'sender_id': USER_ID,
            'receiver_id': receiver_id,
            'thread_id': thread_id
        };
        data = JSON.stringify(data);
        socket.send(data);
        $(this)[0].reset();
    });
};

socket.onmessage = async function(e) {
    let data;
    try {
        data = JSON.parse(e.data);
    } catch (error) {
        console.error('Error parsing message:', error);
        return;
    }
    let message = data['message'];
    let sent_by_id = data['sent_by'];
    let thread_id = data['thread_id'];
    let send_time = data['send_time'];
    let sender_username = data['username'];
    if (!message || !sent_by_id || !thread_id) {
        console.error('Error: Incomplete message data');
        return;
    }
    newMessage(message, sent_by_id, thread_id, send_time, sender_username);
};


socket.onerror = async function(e) {
    console.error('Websocket error: ', e);
};

socket.onclose = async function(e) {
    console.log('close', e);
};

function newMessage(message, sent_by_id, thread_id, send_time, sender_username) {
    if ($.trim(message) === '') {
        return false;
    }
    let message_element;
    let chat_id = 'chat_' + thread_id;

    if(sent_by_id === USER_ID){
        message_element = `
            <div class="d-flex mb-4 replied">
                <div class="msg_cotainer_send">
                    ${message}
                    <span class="msg_time_send">${send_time}</span>
                </div>
                <div class="img_cont_msg">
                    <img src="https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg" class="rounded-circle user_img_msg">
                </div>
            </div>
        `
    } else {
        message_element = `
            <div class="d-flex mb-4 received">
                <div class="img_cont_msg">
                    <img src="https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg" class="rounded-circle user_img_msg">
                </div>
                <div class="msg_cotainer">
                    ${message}
                    <span class="msg_time">${sender_username}, ${send_time}</span>
                </div>
            </div>
        `;
    }

    let message_body = $('.messages-wrapper[chat-id="' + chat_id + '"] .msg_card_body');
    message_body.append($(message_element));
    setTimeout(function() {
        message_body.animate({
            scrollTop: message_body[0].scrollHeight
        }, 100);
    }, 1); // Adjust the delay as needed

    input_message.val(null);
}


$('.contact-li').on('click', function (){
    $('.contacts .active').removeClass('active');
    $(this).addClass('active');

    let chat_id = $(this).attr('chat-id');
    $('.messages-wrapper.is_active').removeClass('is_active');
    let messageWrapper = $('.messages-wrapper[chat-id="' + chat_id +'"]');
    messageWrapper.addClass('is_active');

    // Scroll to the top of the message body
    let messageBody = messageWrapper.find('.msg_card_body');
    messageBody.scrollTop(messageBody[0].scrollHeight);

    let thread_id = chat_id.replace('chat_', '');

    // Make an AJAX call to mark messages as read
    $.ajax({
        url: '/mark_messages_as_read/', // Update this URL to match your URL configuration
        type: 'POST',
        data: {
            'thread_id': thread_id,
            'user_id': USER_ID,
            'csrfmiddlewaretoken': '{{ csrf_token }}' // Include CSRF token for POST requests
        },
        success: function(response) {
            if (response.success) {
                console.log('Messages marked as read');
            } else {
                console.error('Error marking messages as read:', response.error);
            }
        },
        error: function(xhr, status, error) {
            console.error('AJAX error:', error);
        }
    });

});

function get_active_other_user_id(){
    let other_user_id = $('.messages-wrapper.is_active').attr('other-user-id');
    other_user_id = $.trim(other_user_id);
    return other_user_id;
}

function get_active_thread_id(){
    let chat_id = $('.messages-wrapper.is_active').attr('chat-id');
    let thread_id = chat_id.replace('chat_', '');
    return thread_id;
}

$(document).ready(function() {
    $("#searchbar").on("keyup", function() {
        var searchText = $(this).val().toLowerCase();
        $("#contacts .contact-li").each(function() {
            var username = $(this).find(".user_info span").text().toLowerCase();
            if (username.indexOf(searchText) === -1) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    });

    let activeChat = $('.messages-wrapper.is_active');
    if (activeChat.length > 0) {
        let messageBody = activeChat.find('.msg_card_body');
        messageBody.scrollTop(messageBody[0].scrollHeight);
    }

    $(".contact-li").click(function() {
        $(".contact-li").removeClass("active");
        $(this).addClass("active");

        var chatId = $(this).attr("chat-id");
        $(".messages-wrapper").removeClass("is_active").addClass("hide");
        $(".messages-wrapper[chat-id='" + chatId + "']").removeClass("hide").addClass("is_active");
    });
});
