document.addEventListener("DOMContentLoaded", function () {
    const newsletterLink = document.getElementById('newsletter-link');

    // Disable the default click event
    newsletterLink.addEventListener('click', function (event) {
        event.preventDefault();  // Prevent any click action
    });

    // Add a hover event to show an alert
    newsletterLink.addEventListener('mouseover', function () {
        alert("The newsletter feature is not available yet. Please check back soon!");
    });
});

