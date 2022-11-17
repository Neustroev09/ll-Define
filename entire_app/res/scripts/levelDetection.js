var def_lvl_but = document.querySelector("#bt-def-lvl"),
    read_but = document.querySelector("#bt-read"),
    book_lvl_info = document.querySelector("#book-level-info span");

var xhr = new XMLHttpRequest();

function dlbut_click() {
    var cur_url = window.location.href.split('?');
    var t_param = cur_url[cur_url.length - 1];
    xhr.open('GET', '/deflvl?' + t_param);
    xhr.send();
    xhr.onload = function() {
        if (xhr.status != 200) {
            book_lvl_info.textContent = 'XX'
        } else { 
            book_lvl_info.textContent = xhr.response
        }
    };
}

function rdbut_click() {
    var cur_url = window.location.href.split('?');
    var t_param = cur_url[cur_url.length - 1];
    location.href = '/read?' + t_param;
}

def_lvl_but.addEventListener('click', dlbut_click);
read_but.addEventListener('click', rdbut_click);