class RestaurantApp {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.loadMenu();
    }

    initializeElements() {
        // Order elements
        this.orderInput = document.getElementById('orderInput');
        this.orderBtn = document.getElementById('orderBtn');
        this.loading = document.getElementById('loading');
        this.orderResult = document.getElementById('orderResult');
        this.statusBadge = document.getElementById('statusBadge');
        this.aiMessage = document.getElementById('aiMessage');
        this.itemsFound = document.getElementById('itemsFound');
        this.foundItemsList = document.getElementById('foundItemsList');
        this.totalPrice = document.getElementById('totalPrice');
        this.suggestions = document.getElementById('suggestions');
        this.suggestionsList = document.getElementById('suggestionsList');
        this.newOrderBtn = document.getElementById('newOrderBtn');

        // Menu elements
        this.menuContainer = document.getElementById('menuContainer');
    }

    bindEvents() {
        this.orderBtn.addEventListener('click', () => this.submitOrder());
        this.newOrderBtn.addEventListener('click', () => this.resetOrder());
        
        // Allow Enter key to submit order (Ctrl+Enter for textarea)
        this.orderInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                e.preventDefault();
                this.submitOrder();
            }
        });
    }

    async loadMenu() {
        try {
            const response = await fetch('/menu');
            const menu = await response.json();
            this.renderMenu(menu);
        } catch (error) {
            console.error('Error loading menu:', error);
            this.menuContainer.innerHTML = `
                <div class="error-message">
                    <p>Sorry, we couldn't load the menu right now. Please try again later.</p>
                </div>
            `;
        }
    }

    renderMenu(menu) {
        let menuHTML = '';
        
        for (const [category, items] of Object.entries(menu)) {
            menuHTML += `
                <div class="menu-category">
                    <h3 class="category-title">${category.replace('_', ' ')}</h3>
                    <div class="items-list">
                        ${items.map(item => `
                            <div class="item-card">
                                <div class="item-header">
                                    <span class="item-name">${item.name}</span>
                                    <span class="item-price">$${item.price.toFixed(2)}</span>
                                </div>
                                <p class="item-description">${item.description}</p>
                                <span class="availability-badge ${item.available ? 'available' : 'unavailable'}">
                                    ${item.available ? '✓ Available' : '✗ Not Available'}
                                </span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }
        
        this.menuContainer.innerHTML = menuHTML;
    }

    async submitOrder() {
        const orderText = this.orderInput.value.trim();
        
        if (!orderText) {
            this.showError('Please enter your order first!');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch('/order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ order: orderText })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            this.showResult(result);
        } catch (error) {
            console.error('Error submitting order:', error);
            this.showError('Sorry, there was an error processing your order. Please try again.');
        }
    }

    showLoading() {
        this.orderBtn.disabled = true;
        this.loading.classList.remove('hidden');
        this.orderResult.classList.add('hidden');
    }

    showResult(result) {
        this.orderBtn.disabled = false;
        this.loading.classList.add('hidden');
        this.orderResult.classList.remove('hidden');

        // Set status badge
        this.statusBadge.className = `status-badge status-${result.status}`;
        this.statusBadge.textContent = this.getStatusText(result.status);

        // Set AI message
        this.aiMessage.textContent = result.message;

        // Show found items if any
        if (result.items_found && result.items_found.length > 0) {
            this.itemsFound.classList.remove('hidden');
            this.foundItemsList.innerHTML = this.renderItems(result.items_found);
            this.totalPrice.textContent = result.total_price.toFixed(2);
        } else {
            this.itemsFound.classList.add('hidden');
        }

        // Show suggestions if any
        if (result.suggestions && result.suggestions.length > 0) {
            this.suggestions.classList.remove('hidden');
            this.suggestionsList.innerHTML = this.renderItems(result.suggestions);
        } else {
            this.suggestions.classList.add('hidden');
        }

        // Show new order button
        this.newOrderBtn.classList.remove('hidden');
    }

    renderItems(items) {
        return items.map(item => `
            <div class="item-card">
                <div class="item-header">
                    <span class="item-name">${item.name}</span>
                    <span class="item-price">$${item.price.toFixed(2)}</span>
                </div>
                <p class="item-description">${item.description}</p>
                ${item.category ? `<small style="color: #666; font-style: italic;">${item.category.replace('_', ' ')}</small>` : ''}
            </div>
        `).join('');
    }

    getStatusText(status) {
        switch (status) {
            case 'available':
                return '✓ Available';
            case 'partially_available':
                return '⚠ Partially Available';
            case 'unavailable':
                return '✗ Not Available';
            default:
                return 'Unknown';
        }
    }

    showError(message) {
        this.orderBtn.disabled = false;
        this.loading.classList.add('hidden');
        this.orderResult.classList.remove('hidden');

        this.statusBadge.className = 'status-badge status-unavailable';
        this.statusBadge.textContent = '✗ Error';
        this.aiMessage.textContent = message;
        this.itemsFound.classList.add('hidden');
        this.suggestions.classList.add('hidden');
        this.newOrderBtn.classList.remove('hidden');
    }

    resetOrder() {
        this.orderInput.value = '';
        this.orderInput.focus();
        this.orderResult.classList.add('hidden');
        this.newOrderBtn.classList.add('hidden');
        this.orderBtn.disabled = false;
    }
}

// Initialize the app when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new RestaurantApp();
});

// Add some nice animations and interactions
document.addEventListener('DOMContentLoaded', () => {
    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.order-btn, .new-order-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // Add typing indicator effect
    const textarea = document.getElementById('orderInput');
    let typingTimer;
    
    textarea.addEventListener('input', () => {
        clearTimeout(typingTimer);
        textarea.style.borderColor = '#667eea';
        
        typingTimer = setTimeout(() => {
            textarea.style.borderColor = '#e1e1e1';
        }, 1000);
    });
});

// Add CSS for ripple effect
const style = document.createElement('style');
style.textContent = `
    .order-btn, .new-order-btn {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);