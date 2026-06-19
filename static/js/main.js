// Main JavaScript file

document.addEventListener('DOMContentLoaded', function() {
    console.log('Document loaded and ready!');
    
    // Example of a reusable function
    function toggleClass(element, className) {
        if (element.classList.contains(className)) {
            element.classList.remove(className);
            return false;
        } else {
            element.classList.add(className);
            return true;
        }
    }
    
    // Example event listeners can be added here
});