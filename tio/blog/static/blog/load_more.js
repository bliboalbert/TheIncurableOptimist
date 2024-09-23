document.addEventListener("DOMContentLoaded", function () {
    const loadMoreButton = document.getElementById("load-more");

    loadMoreButton.addEventListener("click", function () {
        const page = this.getAttribute("data-page");

        // Make an AJAX request to load more posts
        fetch(`?page=${page}`, {
            headers: {
                "X-Requested-With": "XMLHttpRequest"  // Mark it as an AJAX request
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.posts_html) {
                // Append the new posts to the post list
                document.getElementById("post-list").insertAdjacentHTML("beforeend", data.posts_html);

                // Update the page number for the next request
                loadMoreButton.setAttribute("data-page", parseInt(page) + 1);
            } else {
                // Hide the button if there are no more posts
                loadMoreButton.style.display = "none";
            }
        })
        .catch(error => {
            console.error("Error fetching more posts:", error);
        });
    });
});
