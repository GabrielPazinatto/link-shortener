const API_URL = "http://127.0.0.1:8000/login/"

const submit_btn = document.getElementById('login-btn');
submit_btn.addEventListener('click', login);

async function login(event){
    event.preventDefault();

    try{
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        const response = await fetch(API_URL, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ username: username, password: password })
        });

        const data = await response.json();

        if(response.ok && data.id !== null){
            localStorage.setItem('id', JSON.parse(data).id);
            localStorage.setItem('username', JSON.parse(data).username);
            alert("Login Successful");
            setTimeout(() => {window.location.href = "./user_page.html";}, 500);
        }
    }
    catch(err){
        console.log(err);
        alert(err || "Login Failed");
    }
}