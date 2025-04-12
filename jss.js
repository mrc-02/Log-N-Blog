// jss.js - Connect frontend to backend

// LOGIN
function loginUser() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch("http://localhost:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            localStorage.setItem("user_id", data.user_id);
            localStorage.setItem("username", data.username);
            window.location.href = "profile1.html";
        } else {
            alert(data.message);
        }
    });
}

// REGISTER
function registerUser(username, email, password) {
    fetch("http://localhost:5000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            alert("Registration successful! You can now login.");
            window.location.href = "login fp.html";
        } else {
            alert(data.message);
        }
    });
}

// CREATE POST
function submitPost() {
    const title = document.getElementById("post-title").value;
    const content = document.getElementById("post-content").value;
    const image_url = document.getElementById("post-image").value;
    const user_id = localStorage.getItem("user_id");

    fetch("http://localhost:5000/posts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id, title, content, image_url })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            alert("Post created successfully!");
            window.location.href = "home.html";
        }
    });
}

// LOAD POSTS ON HOME
function loadPosts() {
    fetch("http://localhost:5000/posts")
        .then(res => res.json())
        .then(posts => {
            const container = document.getElementById("posts-container");
            posts.forEach(post => {
                const postDiv = document.createElement("div");
                postDiv.innerHTML = `
                    <h3>${post.title}</h3>
                    <p>by ${post.author}</p>
                    <p>${post.content}</p>
                    <img src="${post.image_url}" alt="post image" width="300">
                    <hr>
                `;
                container.appendChild(postDiv);
            });
        });
}

// PROFILE DISPLAY ON LOAD
function loadProfile() {
    const username = localStorage.getItem("username") || "Guest";
    const email = localStorage.getItem("userEmail") || "Not set";
    document.getElementById("display-name").textContent = username;
    document.getElementById("display-email").textContent = email;
    document.getElementById("edit-name").value = username;
    document.getElementById("edit-email").value = email;
}
