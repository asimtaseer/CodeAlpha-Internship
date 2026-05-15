document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    
    // Set initial greeting time
    document.getElementById('initial-time').textContent = getCurrentTime();

    // Event listener for Send Button
    sendBtn.addEventListener('click', sendMessage);

    // Event listener for Enter Key
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Main function to handle sending messages
    async function sendMessage() {
        const messageText = userInput.value.trim();
        if (messageText === '') return;

        // 1. Add user message to UI
        appendMessage(messageText, 'user');
        
        // Clear input
        userInput.value = '';

        // 2. Add temporary typing indicator for bot
        const typingId = showTypingIndicator();

        try {
            // 3. Send request to Flask API
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: messageText })
            });

            const data = await response.json();
            
            // 4. Remove typing indicator
            removeElement(typingId);

            // 5. Add bot's actual response to UI
            if (response.ok) {
                appendMessage(data.response, 'bot');
            } else {
                appendMessage("Error: Could not connect to the server.", 'bot');
            }

        } catch (error) {
            console.error("Error connecting to backend:", error);
            removeElement(typingId);
            appendMessage("Sorry, the server is currently unreachable. Please try again later.", 'bot');
        }
    }

    // Function to visually append message bubbles
    function appendMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        contentDiv.textContent = text;

        const timeDiv = document.createElement('div');
        timeDiv.classList.add('message-time');
        timeDiv.textContent = getCurrentTime();

        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);

        chatBox.appendChild(messageDiv);
        
        // Scroll to the bottom
        scrollToBottom();
    }

    // Function to show typing animation bubble
    function showTypingIndicator() {
        const id = 'typing-' + Date.now();
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'bot-message');
        messageDiv.id = id;

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        contentDiv.innerHTML = `
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;

        messageDiv.appendChild(contentDiv);
        chatBox.appendChild(messageDiv);
        scrollToBottom();

        return id;
    }

    // Helper functions
    function removeElement(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
});
