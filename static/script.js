document.getElementById('addPostBtn').addEventListener('click', () => {
    document.getElementById('postForm').style.display = 'block';
});

document.getElementById('submissionForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    fetch('/submit', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            e.target.reset();
            document.getElementById('postForm').style.display = 'none';
            loadPosts(); // Refresh the feed
        }
    });
});

// Function to load posts
function loadPosts() {
    fetch('/get_random_posts')
        .then(response => response.json())
        .then(data => {
            const feed = document.getElementById('submissionFeed');
            feed.innerHTML = ''; // Clear existing posts
            data.forEach(post => {
                const item = document.createElement('div');
                item.className = 'post';
                item.innerHTML = `
                    <p>${post.text}</p>
                    <img src="${post.file}" alt="User submission" style="max-width: 100%;">
                    <span class="like-btn" onclick="likePost('${post.id}')">Like (${post.likes})</span>
                `;
                feed.appendChild(item);
            });
        });
}

// Function to like a post
function likePost(postId) {
    fetch(`/like/${postId}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        loadPosts(); // Refresh the feed to show updated likes
    });
}

// Initial load of posts
loadPosts();
