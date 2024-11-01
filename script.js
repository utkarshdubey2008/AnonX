document.addEventListener("DOMContentLoaded", () => {
    const postForm = document.getElementById("postForm");
    const postsContainer = document.getElementById("postsContainer");

    postForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const content = document.getElementById("content").value;
        const fileLink = document.getElementById("fileLink").value;

        const response = await fetch("/api/posts", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ content, fileLink }),
        });

        if (response.ok) {
            postForm.reset();
            fetchPosts();
        } else {
            alert("Error posting your content.");
        }
    });

    async function fetchPosts() {
        const response = await fetch("/api/posts");
        const posts = await response.json();
        postsContainer.innerHTML = ""; // Clear previous posts

        posts.forEach(post => {
            const postElement = document.createElement("div");
            postElement.classList.add("post");
            postElement.innerHTML = `
                <p>${post.content}</p>
                ${post.fileLink ? `<a href="${post.fileLink}" target="_blank">View File</a>` : ""}
            `;
            postsContainer.appendChild(postElement);
        });
    }

    // Load posts when the page loads
    fetchPosts();
});
