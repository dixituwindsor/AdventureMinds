document.addEventListener('DOMContentLoaded', function() {
    // Fetch users and populate the user list
    fetch('/get_users/')
        .then(response => response.json())
        .then(users => {
            const userList = document.getElementById('user-list');
            users.forEach(user => {
                const listItem = document.createElement('li');
                listItem.textContent = user.username;
                listItem.addEventListener('click', () => {
                    // Handle user selection
                    startChatWithUser(user.id);
                });
                userList.appendChild(listItem);
            });
        });

    // Function to start a chat with a user
    function startChatWithUser(userId) {
        // Close the user selection modal
        $('#userSelectModal').modal('hide');

        // Update the WebSocket URL to point to a private chat with the selected user
        const socketUrl = `ws://${window.location.host}/ws/chat/private/${userId}/`;
        const socket = new WebSocket(socketUrl);

        // Update the rest of your WebSocket handling code to work with private chats
        // This includes sending and receiving messages, updating the UI, etc.
        socket.addEventListener('open', function(event) {
            console.log('Connection opened');
        });

        socket.addEventListener('message', function(event) {
            const message = JSON.parse(event.data);
            const messageElement = document.createElement('p');
            messageElement.textContent = message.message;
            document.getElementById('chat-messages').appendChild(messageElement);
        });

        document.getElementById('send-message-btn').addEventListener('click', function() {
            const messageText = document.getElementById('message-text').value;
            socket.send(JSON.stringify({
                'message': messageText
            }));
            document.getElementById('message-text').value = '';
        });
    }

    // Example function to create a group (not fully implemented)
    document.getElementById('create-group-btn').addEventListener('click', function() {
        // Implement group creation logic here
    });
});
