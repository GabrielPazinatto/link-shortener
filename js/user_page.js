
const user_id = localStorage.getItem('id');
const table = document.getElementById('table');
const shorten_link_btn = document.getElementById('shorten-btn');
const delete_selected_btn = document.getElementById('delete-btn');
const API_URL = "https://link-shortener-9ffo.vercel.app/user/";

const REDIRECT_URL = "https://shortify.rf.gd/"

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
        
        console.log(data)

        if(!response.ok){
            alert("Failed to add new URL!");
            return;
        }
        
        alert("URL added successfully!");
    }
    
    catch(err){
        console.log(err);
        alert("Failed to add new URL" || err);
    }

    location.reload();

}

function add_url_table_row(entry, row_count){
    let new_row = table.insertRow(-1);
        
    let count_row = new_row.insertCell(0);
    let url_cell = new_row.insertCell(1);
    let short_url_cell = new_row.insertCell(2);

    let checkbox_cell = new_row.insertCell(3);
    let checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.classList.add('checkbox'); 
    checkbox_cell.appendChild(checkbox);

    count_row.innerHTML = row_count;
    url_cell.innerHTML = "<a href='" + entry.url + "'>" + entry.url + "</a>";
    short_url_cell.innerHTML = "<a href='" + REDIRECT_URL + entry.short_url + "'>" + REDIRECT_URL + entry.short_url + "</a>";
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

        json_data = JSON.parse(data);

        if(Array.isArray(json_data)){
            var row_count = 1;
            json_data.forEach(entry => {
                add_url_table_row(entry, row_count);
                row_count++;
            });
        }
        else{        
            add_url_table_row(json_data, 1);
        };
    }
    catch(err){
        console.log(err);
        alert("Failed to get user data");
    }
}

if(localStorage['id'] == undefined || localStorage['id'] == null){
    setTimeout(() => {window.location.href = "./login.html";}, 500);   
}

function get_selected_short_urls(){
    var selected_urls = new Array();
    const checkboxes = document.querySelectorAll('.checkbox');

    checkboxes.forEach(checkbox => {
        if(checkbox.checked){
            selected_urls.push(checkbox.parentElement.parentElement.cells[2].innerText);
        }
    });

    return selected_urls;
}

async function delete_selected(event){
    event.preventDefault();

    var selected_urls = get_selected_short_urls();
    const user_id = localStorage.getItem('id');

    try{
        const response = await fetch(`${API_URL}${user_id}/delete_url/`,{
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({urls:selected_urls})
        });
    
        data = await response.json();

        if(!response.ok){
            alert("Failed to delete selected URLs!");
            location.reload();
            return;
        }
    }

    catch(err){
        console.log(err);
        alert("Failed to delete selected URLs" || err);
        location.reload()
        return;
    }

    location.reload();

}

shorten_link_btn.addEventListener('click', add_new_url);
delete_selected_btn.addEventListener('click', delete_selected);
