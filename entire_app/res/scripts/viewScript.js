var first_book_page = 0;
		
var page_viewer = document.querySelector("#viewer"),
    view_panel = document.querySelector("#view_panel");

range_slider = document.createElement('input');
range_slider.className = 'rn_sldr';

range_slider.setAttribute('type', 'range');
range_slider.setAttribute('min', 1);
range_slider.setAttribute('max', last_book_page + 1);
range_slider.value = 1;

page_number = document.createElement('input')
page_number.className = 'page_num';
page_number.value = 1;

page_number.setAttribute('type', 'text');

page_txt = document.createElement('span');
page_txt.className = 'book_len';
page_txt.innerHTML = 'Страница';

book_len = document.createElement('span');
book_len.className = 'book_len';
book_len.innerHTML = ' из ' + (last_book_page + 1);
        
var current_page = 0;

function update_page_number() {
    page_number.value = current_page + 1
}

function update_range_slider () {
    range_slider.value = current_page + 1
}

function render_viewer() {

    page_viewer.innerHTML = '';
    
    var page_container = document.createElement('div');
    page_container.className = 'page_con'
    
    var xhr = new XMLHttpRequest();
    function book_page_load() {
        var cur_url = window.location.href.split('?');
        var t_param = cur_url[cur_url.length - 1];
        xhr.open('GET', '/pc?' + t_param + '&pn=' + current_page);
        xhr.send();
        xhr.onload = function render_page() {
            if (xhr.status != 200) {
                page_container.textContent = '404'
            } else { 
                json_page = JSON.parse(xhr.response);
                console.log(json_page);
                flat_html_page = '';
                is_in_parag = false;
                for (var key in json_page) {
                    if (json_page.hasOwnProperty(key)) {
                        if (json_page[key].substring(0, 2) == "\n\n") {
                            if (is_in_parag) {
                                flat_html_page += '</p><p>';
                            } else {
                                is_in_parag = true;
                                flat_html_page += '<p>';
                            }
                        }
                        flat_html_page += '<span name="s' + key + '">' + json_page[key].trim().replace('\n\n', '<br>') + '.</span>';
                    }
                }
                if (is_in_parag) {
                    flat_html_page += '</p>';
                }
                page_container.innerHTML = flat_html_page;
                
                page_viewer.appendChild(page_container);
                
                function next_page(){
                    if (current_page < last_book_page) {
                        current_page += 1;
                        update_range_slider();
                        update_page_number();
                        render_viewer();
                    }
                }
                
                function previous_page(){
                    if (current_page > 0) {
                        current_page -= 1;
                        update_range_slider();
                        update_page_number();
                        render_viewer();
                    }
                }
                
                var buttons_panel = document.createElement('div');
                buttons_panel.className = 'but_pan';
                
                if (current_page >= 0) {
                    var prev_page_but = document.createElement('span');
                    prev_page_but.className = 'cng_page';
                    prev_page_but.innerHTML = '<< Назад';
                    prev_page_but.addEventListener('click', previous_page);
                    buttons_panel.appendChild(prev_page_but);
                }

                buttons_panel.appendChild(range_slider);
                
                if (current_page <= last_book_page) {
                    var next_page_but = document.createElement('span');
                    next_page_but.className = 'cng_page';
                    next_page_but.innerHTML = 'Далее >>';
                    next_page_but.addEventListener('click', next_page);
                    buttons_panel.appendChild(next_page_but);
                }
                
                page_viewer.appendChild(buttons_panel);
                
            }
        };
    }
    book_page_load();	
}

render_viewer();

range_slider.addEventListener("input", () => {
    range_slider.setAttribute('title', range_slider.value);
    current_page = range_slider.value - 1;
    update_page_number();
    render_viewer();
});

page_number.addEventListener("keydown", (e) => {
    if (e.key == "Enter") {
        if (page_number.value < 1) {
            page_number.value = 1;
        } else if (page_number.value > last_book_page) {
            page_number.value = last_book_page + 1;
        }
        current_page = page_number.value - 1;
        update_range_slider();
        render_viewer();
    }
});

view_panel.appendChild(page_txt);
view_panel.appendChild(page_number);
view_panel.appendChild(book_len);