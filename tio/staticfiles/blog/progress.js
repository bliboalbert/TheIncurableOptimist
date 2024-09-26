// Function to update the progress bar based on scroll position
function updateProgressBar() {
    // Get the current scroll position and document height
    var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    var scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    var scrollPercentage = (scrollTop / scrollHeight) * 100;

    // Update the width of the progress bar
    document.getElementById("progressBar").style.width = scrollPercentage + "%";
}

// Wait until the DOM is fully loaded before adding the event listener
document.addEventListener("DOMContentLoaded", function() {
    // Listen for the scroll event and call updateProgressBar when scrolling
    window.addEventListener('scroll', updateProgressBar);
});
