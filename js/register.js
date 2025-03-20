const API_URL = "link-shortener-9ffo.vercel.app/register"

const submit_btn = document.getElementById('submit-btn');
submit_btn.addEventListener('click', register);

function validate_form(username, password, cpassword){
    if(username === "" || password === "" || cpassword === ""){
        alert("Please fill in all fields");
        return false;
    }

    if(username.length < 4 || username.length > 20){
        alert("Username must be between 4 and 20 characters");
        return false;
    }

    if(password.length < 4 || password.length > 20){
        alert("Password must be between 4 and 20 characters");
        return false
    }
    
    else if(password !== cpassword){
        alert("Passwords do not match");
        return false;
    }

    return true;
}
    
async function register(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const cpassword = document.getElementById('cpassword').value;
    
    if(!validate_form(username, password, cpassword)){
        return;
    }

    try{
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ username: username, password: password })
        });

        const data = await response.json();
        if(response.ok){
            alert("Registration Successful");
            setTimeout(() => {window.location.href = "./login.html";}, 500);          
        }
        else{
            alert(data.message || "Username already exists");
        }
    }
    catch(err){
        console.log(err);
        alert(data.message || "Registration Failed");
    }
}