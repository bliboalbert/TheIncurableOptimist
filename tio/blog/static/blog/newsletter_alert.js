document.addEventListener("DOMContentLoaded", function () {
    const newsletterForm = document.getElementById("newsletter-form");
    const newsletterLink = document.getElementById("newsletter-link");

    if (newsletterForm) {
        newsletterForm.addEventListener("submit", function (event) {
            event.preventDefault();  // Prevent form submission for now
            alert("The newsletter feature is not available yet. Please check back soon!");
        });
    }
});
