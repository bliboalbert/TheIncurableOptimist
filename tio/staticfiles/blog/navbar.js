document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById('navbar-toggle');
    const navLinks = document.getElementById('nav-link');

    toggleButton.addEventListener('click', function () {
        navLinks.classList.toggle('show');
    });
});
