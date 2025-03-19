
const user_id = localStorage.getItem('id');
const table = document.getElementById('table');
const shorten_link_btn = document.getElementById('shorten-btn');
const API_URL = "http://127.0.0.1:8000/user/";


window.onload = async function(){
    get_user_data();
}

async function add_new_url(event){
    event.preventDefault();
    
    const user_id = localStorage.getItem('id');
    const url = document.getElementById('url-input').value;

    console.log(JSON.stringify({text: url}));

    try{
        const response = await fetch(`${API_URL}${parseInt(user_id)}/add_url/`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({text:url})
        });
        
        const data = await response.json();
        
        if(!data.ok){
            alert("Failed to add new URL!");
            return;
        }
        
        alert("URL added successfully!");
    }
    
    catch(err){
        console.log(err);
        alert("Failed to add new URL" || err);
    }
}


async function get_user_data(){
    try{
    
        const user_id = localStorage.getItem('id');
        const response = await fetch(`${API_URL}${user_id}/get_data/`);
        
        const data = await response.json();
        
        if(!response.ok){
            alert("Failed to get user data!");
            return;
        }
        
        table.innerHTML = "";
        var i = 1;
        JSON.parse(data).forEach(entry => {
            let new_row = table.insertRow(-1);
            let count_row = new_row.insertCell(0);
            let link_cell = new_row.insertCell(1);
            let short_link_cell = new_row.insertCell(2);
            
            count_row.innerHTML = i++;
            link_cell.innerHTML = "<a href = " +entry.url + ">" + entry.url + "</a>";
            short_link_cell.innerHTML = "<a href = " +entry.short_url + ">" + entry.short_url + "</a>";
        });
        
    }
    catch(err){
        console.log(err);
        alert("Failed to get user data");
    }
}

if(localStorage['id'] == undefined || localStorage['id'] == null){
    setTimeout(() => {window.location.href = "./login.html";}, 500);   
}

shorten_link_btn.addEventListener('click', add_new_url);