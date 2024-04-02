
document.addEventListener("DOMContentLoaded", function() {
    const dropdown = document.querySelector('.multiselect-dropdown select');
    const selectedOptions = document.querySelector('.multiselect-dropdown .selected-options');

    dropdown.addEventListener("change", function() {
        const selected = Array.from(dropdown.selectedOptions).map(option => option.text);
        selectedOptions.textContent = selected.join(', ');
    });
});
