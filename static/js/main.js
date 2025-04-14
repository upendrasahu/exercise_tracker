// Exercise Tracker JavaScript

// Set the current year for the footer copyright
document.addEventListener('DOMContentLoaded', function() {
    const currentYearElement = document.querySelector('.container p');
    if (currentYearElement) {
        const currentYear = new Date().getFullYear();
        currentYearElement.innerHTML = currentYearElement.innerHTML.replace('{{ current_year }}', currentYear);
    }

    // Set default value of date input to today if on add exercise page
    const dateInput = document.getElementById('date');
    if (dateInput && !dateInput.value) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.value = today;
    }
});