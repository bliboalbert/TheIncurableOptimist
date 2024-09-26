document.addEventListener("DOMContentLoaded", function () {
    const loadMoreButton = document.getElementById("load-more");
    const loadLessButton = document.getElementById("load-less");
    const postList = document.getElementById("post-list");

    loadLessButton.style.display = "none";

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

                // Check if we have loaded the last page
                if (!data.has_next) {
                    loadMoreButton.style.display = "none";
                    loadLessButton.style.display = "block";
                }
            }
        })
        .catch(error => {
            console.error("Error fetching more posts:", error);
        });
    });

        // Load Less Functionality
        loadLessButton.addEventListener("click", function () {
            postList.innerHTML = ""; // Clear all loaded posts

            // Reload the first page of posts
            fetch(`?page=1`, {
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                postList.insertAdjacentHTML("beforeend", data.posts_html);
                loadLessButton.style.display = "none";
                loadMoreButton.style.display = "block";
                loadMoreButton.setAttribute("data-page", 2);
            })
            .catch(error => {
                console.error("Error loading less posts:", error);
            });
        });
});