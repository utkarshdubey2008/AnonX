const postForm = document.getElementById('postForm');
const feed = document.getElementById('feed');

postForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const content = document.getElementById('content').value;
    const fileLink = document.getElementById('fileLink').value;

    const post = {
        content: content,
        file_link: fileLink,
        timestamp: new Date().toISOString()
    };

    const response = await fetch('/api/posts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(post),
    });

    if (response.ok) {
        loadPosts();
        postForm.reset();
    }
});

async function loadPosts() {
    const response = await fetch('/api/posts');
    const posts = await response.json();
    feed.innerHTML = posts.map(post => `
        <div class="post">
            <p><strong>${post.timestamp}</strong></p>
            <p>${post.content}</p>
            ${post.file_link ? `<a href="${post.file_link}" target="_blank">View File</a>` : ''}
            <p>${post.likes} likes</p>
        </div>
    `).join('');
}

loadPosts();
