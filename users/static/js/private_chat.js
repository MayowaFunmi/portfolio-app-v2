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
    var display_chats = $('.msg_card_body')

    setInterval(function() {
        $.ajax({
            url: '/chat/get_private_messages/',
            data: {
                'sender': sender,
                'receiver': receiver
            },
            dataType: 'json',
            success: function(data) {
                console.log(data)
                display_chats.empty();
                var data_msg = data.private_details
                    // separate sender from receiver chats
                if (active_user == sender) {
                    data_msg.map(x => {
                        display_chats.append(`
                            <div class="d-flex justify-content-end mb-4">
                                <div class="msg_cotainer_send">
                                    ${x.message}
                                    <span class="msg_time">${x.date}</span>
                                </div>
                            </div>
                        `)
                    })
                } else {
                    data_msg.map(x => {
                        display_chats.append(`
                            <div class="d-flex justify-content-start mb-4">
                                <div class="msg_cotainer">
                                    ${x.message}
                                    <span class="msg_time">${x.date}</span>
                                </div>
                            </div>
                        `)
                    })
                }
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