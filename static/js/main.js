// Modern JavaScript for Urban Orientation Platform

document.addEventListener('DOMContentLoaded', function() {
    // Add smooth animations to page elements
    animateOnScroll();

    // Initialize chat functionality
    initializeChat();

    // Initialize form interactions
    initializeFormInteractions();

    console.log('Urban Orientation Platform loaded with modern enhancements');
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
    const container = document.querySelector('.chat-messages');
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}

// Initialize chat functionality when DOM is loaded
function initializeChat() {
    scrollToBottom();

    // Add typing animation effect for bot messages
    addTypingAnimation();
}

// Add typing animation effect for bot messages
function addTypingAnimation() {
    // This would be implemented to show typing indicators in a real app
    console.log('Bot typing animation initialized');
}

// Initialize form interactions
function initializeFormInteractions() {
    // Add focus effects to form inputs
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
}

// Animate elements as they come into view
function animateOnScroll() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements with animate-on-scroll class
    const elements = document.querySelectorAll('.animate-on-scroll');
    elements.forEach(element => {
        observer.observe(element);
    });
}

// Add form validation and styling
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required], textarea[required]');
            let isValid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    input.classList.add('is-invalid');
                    isValid = false;
                } else {
                    input.classList.remove('is-invalid');
                    input.classList.add('is-valid');
                }
            });

            if (!isValid) {
                e.preventDefault();
            }
        });
    });
}

// Initialize form validation when DOM loads
document.addEventListener('DOMContentLoaded', initializeFormValidation);

// Parallax effect for hero sections
function initializeParallax() {
    const heroSections = document.querySelectorAll('.hero-section');
    window.addEventListener('scroll', function() {
        heroSections.forEach(hero => {
            const scrolled = window.pageYOffset;
            const rate = hero.getAttribute('data-speed') || 0.5;
            const yPos = -(scrolled * rate);
            hero.style.transform = `translateY(${yPos}px)`;
        });
    });
}

// Initialize parallax effect if hero sections exist
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.hero-section')) {
        initializeParallax();
    }
});