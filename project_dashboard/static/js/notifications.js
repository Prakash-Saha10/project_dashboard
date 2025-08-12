// Connect to WebSocket
const notificationSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/notifications/'
);

// Update notification count in navbar
notificationSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const badge = document.getElementById('unread-count');
    
    if (badge) {
        const currentCount = parseInt(badge.textContent) || 0;
        badge.textContent = currentCount + 1;
        
        // Play sound
        const audio = new Audio('/static/sounds/notification.mp3');
        audio.play().catch(e => console.log("Audio play failed:", e));
        
        // Add to dropdown
        const dropdown = document.querySelector('.notification-dropdown');
        if (dropdown) {
            const newNotification = document.createElement('a');
            newNotification.className = 'dropdown-item notification-item unread';
            newNotification.innerHTML = `
                ${data.message}
                <small class="text-muted">just now</small>
            `;
            dropdown.insertBefore(newNotification, dropdown.firstChild.nextSibling);
        }
    }
};

// Mark notifications as read
document.querySelectorAll('.notification-item').forEach(item => {
    item.addEventListener('click', function() {
        const notificationId = this.dataset.id;
        if (notificationId) {
            fetch(`/notifications/${notificationId}/read/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            });
        }
    });
});

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}