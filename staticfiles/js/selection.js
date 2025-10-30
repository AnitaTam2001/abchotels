// static/js/selection.js
document.addEventListener('DOMContentLoaded', function() {
    // Room selection functionality
    const roomSelections = document.querySelectorAll('.room-selection');
    roomSelections.forEach(room => {
        room.addEventListener('click', function() {
            roomSelections.forEach(r => r.classList.remove('selected'));
            this.classList.add('selected');
        });
    });

    // Amenity selection functionality
    const amenityOptions = document.querySelectorAll('.amenity-option');
    amenityOptions.forEach(amenity => {
        amenity.addEventListener('click', function() {
            this.classList.toggle('selected');
            const checkbox = this.querySelector('.amenity-checkbox');
            checkbox.checked = !checkbox.checked;
        });
    });

    // Package selection functionality
    const packageOptions = document.querySelectorAll('.package-option');
    packageOptions.forEach(pkg => {
        pkg.addEventListener('click', function() {
            packageOptions.forEach(p => p.classList.remove('selected'));
            this.classList.add('selected');
        });
    });

    // Contact preference selection
    const contactPreferences = document.querySelectorAll('.contact-preference');
    contactPreferences.forEach(pref => {
        const radio = pref.querySelector('input[type="radio"]');
        
        pref.addEventListener('click', function() {
            contactPreferences.forEach(p => p.classList.remove('selected'));
            this.classList.add('selected');
            radio.checked = true;
        });
        
        if (radio.checked) {
            pref.classList.add('selected');
        }
    });

    // Real-time price calculation for booking form
    const checkInInput = document.querySelector('input[name="check_in"]');
    const checkOutInput = document.querySelector('input[name="check_out"]');
    const priceDisplay = document.querySelector('.price-calculation');
    
    if (checkInInput && checkOutInput && priceDisplay) {
        function calculatePrice() {
            const checkIn = new Date(checkInInput.value);
            const checkOut = new Date(checkOutInput.value);
            
            if (checkIn && checkOut && checkOut > checkIn) {
                const nights = Math.ceil((checkOut - checkIn) / (1000 * 60 * 60 * 24));
                const pricePerNight = parseFloat(priceDisplay.dataset.price);
                const totalPrice = nights * pricePerNight;
                
                priceDisplay.innerHTML = `
                    <strong>Total for ${nights} night${nights !== 1 ? 's' : ''}: $${totalPrice.toFixed(2)}</strong>
                `;
            }
        }
        
        checkInInput.addEventListener('change', calculatePrice);
        checkOutInput.addEventListener('change', calculatePrice);
    }
});

// Filter and sort functionality
function applyFilters() {
    const form = document.querySelector('.filter-form');
    if (form) {
        form.submit();
    }
}

function clearFilters() {
    const inputs = document.querySelectorAll('.filter-input, .filter-select');
    inputs.forEach(input => {
        if (input.type === 'text' || input.type === 'number') {
            input.value = '';
        } else if (input.tagName === 'SELECT') {
            input.selectedIndex = 0;
        }
    });
    applyFilters();
}