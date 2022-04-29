$(document).ready(function() {
    $('#action_menu_btn').click(function() {
        $('.action_menu').toggle();
    });
    var sender = $('input[name="sender"]').val();
    var receiver = $('input[name="receiver"]').val();
    var active_user = $('input[name="active_user"]').val()

    //var chatId = $('input[name="room_id"]').val();
    //var message = $('textarea#message').val();
    //var display_chats = $('#display_chats')
    var display_chats = $('.msger-chat')

    setInterval(function() {
        $.ajax({
            url: '/chat/get_private_messages/',
            data: {
                'sender': sender,
                'receiver': receiver
            },
            dataType: 'json',
            success: function(data) {
                console.log('active_user = ', active_user)
                console.log('sender = ', sender)
                console.log('receiver = ', receiver)

                display_chats.empty();
                var data_msg = data.private_details
                    // separate sender from receiver chats

                data_msg.map(x => {
                    display_chats.append(`
                        <div class="msg right-msg">
                            <div class="msg-bubble">
                                <div class="msg-info">
                                    <div class="msg-info-name">${receiver}</div>
                                    <div class="msg-info-time">${x.date}</div>
                                </div>
        
                                <div class="msg-text">
                                    ${x.message}
                                </div>
                            </div>
                        </div>

                    `)
                })

            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
            }
        })
    }, 1000);

    // save private messages from private chat page
    $('form#private_form').submit(function(e) {
        e.preventDefault()
        var msg = $('input[name="message"]').val()
        $.ajax({
            url: "/chat/save_private/",
            data: {
                'sender': sender,
                'receiver': receiver,
                'message': msg,
            },
            dataType: 'json',
            success: function(data) {
                console.log(data.private_msg)
                $('input[name="message"]').val('')
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
            }
        })
    })
})