// JavaScript for Urban Orientation Platform

// Mobile navigation toggle
document.addEventListener('DOMContentLoaded', function() {
    // Add any JavaScript functionality here
    console.log('Urban Orientation Platform loaded');
});

// Function to handle chat messages
function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (message) {
        // In a real implementation, this would send the message to the server
        console.log('Sending message:', message);
        messageInput.value = '';
    }
}

// Handle Enter key press in message input
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Auto-scroll conversation to bottom
function scrollToBottom() {
    const container = document.querySelector('.conversation-container');
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}

// Initialize chat functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    scrollToBottom();
});