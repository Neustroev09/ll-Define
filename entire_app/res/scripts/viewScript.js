
var gl_translate_tooltip_visible = false,
	gl_translate_tooltip_dom_obj = null,
	gl_real_sr = '',
	gl_page_container_obj = null;

function some_script(last_book_page) {
	
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

	var page_container = null;
	
	var T_server_response = null,
		T_flat_page = '',
		T_flat_page_with_words = '',
		T_flat_page_with_sens = '';
	
	function add_words_to_json(json_page) {
		var new_page_obj = {},
			word_counter = 0,
			old_sen_ver = '';
		for (var key in json_page) {
			if (json_page.hasOwnProperty(key)) {
				var matches = json_page[key].matchAll(/((?=\S*[\u2019'-])([a-zA-Z\u2019'-]+)|\b(\w+?)\b)/ig),
					prev_match_indx = 0;
				rest = '';
				for (const match of matches) {
					rest += json_page[key].substring(prev_match_indx, match.index);
					rest += '<span class="page_word w' + word_counter + '" onclick="click_page_word(\'w' + word_counter + '\')">' + match[0] + '</span>'
					prev_match_indx = match.index + match[0].length;
					word_counter += 1;
				}
				rest += json_page[key].substring(prev_match_indx, json_page[key].length);
				new_page_obj[key] = rest;
			}
		}
		return new_page_obj;
	}

	function book_page_load() {
		var cur_url = window.location.href.split('?');
		var t_param = cur_url[cur_url.length - 1];
		var xhr = new XMLHttpRequest();
		xhr.open('GET', '/pc?' + t_param + '&pn=' + current_page);
		xhr.send();
		xhr.onload = function render_page() {
			if (xhr.status != 200) {
				page_container.textContent = '404'
			} else { 
				gl_real_sr = xhr.response;
				T_server_response = JSON.parse(xhr.response);
				T_flat_page = json_to_flat(T_server_response);
				page_container.innerHTML = T_flat_page;
			}
		}
	}

	function render_viewer() {

		page_viewer.innerHTML = '';
		
		var upper_button_panel = document.createElement('div');
		upper_button_panel.className = 'upp_but_pan';
		
		var translate_button_ch = document.createElement('input'),
			check_grammar_button_ch = document.createElement('input'),
			translate_button_lb = document.createElement('label'),
			check_grammar_button_lb = document.createElement('label'),
			translate_button = document.createElement('div'),
			check_grammar_button = document.createElement('div');
			
		translate_button_ch.setAttribute('type', 'checkbox');
		check_grammar_button_ch.setAttribute('type', 'checkbox');
		
		function swich_to_translate_feature()     { if (check_grammar_button_ch.checked) { check_grammar_button_ch.checked = false } }
		function swich_to_check_grammar_feature() { if (translate_button_ch.checked)     { translate_button_ch.checked = false } }
		
		function disable_all_features() {
			translate_button_ch.checked = false;
			check_grammar_button_ch.checked = false;
			T_flat_page_with_words = '';
			T_flat_page_with_sens = '';
		}
		
		function translate_button_ch_event() {
			if (translate_button_ch.checked) {
				swich_to_translate_feature();
				if (T_flat_page_with_words != '') {
					page_container.innerHTML = T_flat_page_with_words;
				} else {
					T_flat_page_with_words = json_to_flat(add_words_to_json(T_server_response));
					page_container.innerHTML = T_flat_page_with_words;
				}
			} else {
				page_container.innerHTML = T_flat_page;
			}
		}
		
		function check_grammar_button_ch_event() {
			if (check_grammar_button_ch.checked) {
				swich_to_check_grammar_feature();
				if (T_flat_page_with_sens != '') {
					page_container.innerHTML = T_flat_page_with_sens;
				} else {
					T_flat_page_with_sens = json_to_flat(T_server_response, true);
					page_container.innerHTML = T_flat_page_with_sens;
					//console.log('pizdec');
				}
			} else {
				page_container.innerHTML = T_flat_page;
			}
		}
		
		translate_button_ch.addEventListener('change', translate_button_ch_event);
		check_grammar_button_ch.addEventListener('change', check_grammar_button_ch_event);
		
		translate_button_ch.setAttribute('id', 'tr_button');
		check_grammar_button_ch.setAttribute('id', 'chgr_button');
		
		translate_button_lb.setAttribute('for', 'tr_button');
		check_grammar_button_lb.setAttribute('for', 'chgr_button');
		
		translate_button_lb.innerHTML = "Перевести слово";
		check_grammar_button_lb.innerHTML = "Определить время";
		
		translate_button.setAttribute('class', 'ubp_el');
		check_grammar_button.setAttribute('class', 'ubp_el');
		
		translate_button.appendChild(translate_button_ch);
		translate_button.appendChild(translate_button_lb);
		upper_button_panel.appendChild(translate_button);
		
		check_grammar_button.appendChild(check_grammar_button_ch);
		check_grammar_button.appendChild(check_grammar_button_lb);
		upper_button_panel.appendChild(check_grammar_button);
		
		page_viewer.appendChild(upper_button_panel);
		
		page_container = document.createElement('div');
		page_container.className = 'page_con'
		
		page_viewer.appendChild(page_container);
		gl_page_container_obj = page_container;
		
		function contol_update() {
			update_range_slider();
			update_page_number();
			book_page_load();
			disable_all_features();
		}
		
		function next_page(){
			if (current_page < last_book_page) {
				current_page += 1;
				contol_update();
			}
		}
		
		function previous_page(){
			if (current_page > 0) {
				current_page -= 1;
				contol_update();
			}
		}

		var bottom_button_panel = document.createElement('div');
		bottom_button_panel.className = 'but_pan';
		
		if (current_page >= 0) {
			var prev_page_but = document.createElement('span');
			prev_page_but.className = 'cng_page';
			prev_page_but.innerHTML = '<< Назад';
			prev_page_but.addEventListener('click', previous_page);
			bottom_button_panel.appendChild(prev_page_but);
		}

		bottom_button_panel.appendChild(range_slider);
		
		if (current_page <= last_book_page) {
			var next_page_but = document.createElement('span');
			next_page_but.className = 'cng_page';
			next_page_but.innerHTML = 'Далее >>';
			next_page_but.addEventListener('click', next_page);
			bottom_button_panel.appendChild(next_page_but);
		}
		
		page_viewer.appendChild(bottom_button_panel);
		
		book_page_load();	
		
		return [disable_all_features];
	}

	ex_update_features = render_viewer();
	
	function exec_euf() {
		for (var i = 0; i < ex_update_features.length; i++) { ex_update_features[i]() }
	}

	range_slider.addEventListener("input", () => {
		range_slider.setAttribute('title', range_slider.value);
		current_page = range_slider.value - 1;
		update_page_number();
		book_page_load();
		exec_euf();
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
			book_page_load();
			exec_euf();
		}
	});

	view_panel.appendChild(page_txt);
	view_panel.appendChild(page_number);
	view_panel.appendChild(book_len);
}



function click_page_word (word) {
	
	if (gl_translate_tooltip_visible) {
		gl_translate_tooltip_dom_obj.remove();
		gl_translate_tooltip_dom_obj = null;
	}

	var word_el = document.querySelector('.' + word),
		tooltip = document.createElement('span');
	
	tooltip.setAttribute('class', 'page_word_tooltip');
	
	tooltip.innerHTML = 'перевод ...';
	
	var cur_url = window.location.href.split('?');
	var t_param = cur_url[cur_url.length - 1];
	var xhr = new XMLHttpRequest();
	xhr.open('GET', '/e2r?' + t_param + '&w=' + word_el.innerHTML);
	console.log('/e2r?' + t_param + '&w=' + word_el.innerHTML)
	xhr.send();
	xhr.onload = function render_page() {
		if (xhr.status != 200) {
			tooltip.innerHTML = 'Some Error'
		} else { 
			tooltip.innerHTML = xhr.response;
			word_el.appendChild(tooltip);
			tooltip.style.opacity = '1';
			tooltip.style.left = - (tooltip.offsetWidth - word_el.offsetWidth) / 2 + 'px';
		}
	}
	
	var tool_tip_show = true,
		tool_tip_show_timer_id = null;
		
	word_el.onmouseover = function() {
		if (tooltip) {
			if (tool_tip_show_timer_id) {
				clearTimeout(tool_tip_show_timer_id);
				tool_tip_show_timer_id = null;
			}
			tooltip.style.opacity = '1';
		}
	} 
	word_el.onmouseout = function() {
		if (tooltip) {
			tool_tip_show_timer_id = setTimeout(function(){
				tooltip.style.opacity = '0'; 
			}, 500);
		}
	} 
	
	gl_translate_tooltip_visible = true;
	gl_translate_tooltip_dom_obj = tooltip;
}

function click_page_sen (word) {
	var s_num = word.substring(1),
		s_el = document.querySelector('.' + word);
	var cur_url = window.location.href.split('?');
	var t_param = cur_url[cur_url.length - 1];
	var xhr = new XMLHttpRequest();
	xhr.open('GET', '/gr?' + t_param + '&s=' + s_num);
	console.log('/gr?' + t_param + '&s=' + s_num)
	xhr.send();
	xhr.onload = function render_page() {
		if (xhr.status != 200) {
			console.log('Some Error')
		} else { 
			gr_ts = JSON.parse(xhr.response);
			page_j = JSON.parse(gl_real_sr);
			prev_match_indx = 0;
			new_sen = '';
			word_counter = 0;
			for (const t of gr_ts) {
				cur_cl = 'tnswn' + word_counter
				new_sen += page_j[s_num].substring(prev_match_indx, t['index'][0]);
				new_sen += '<span class="tnsw0 ' + cur_cl + '" onmouseover="mov_tt(\'' + cur_cl + '\')" onmouseout="mou_tt(\'' + cur_cl + '\')" style="background:' + getRandomColor() + ';">' +
								page_j[s_num].substring(t['index'][0], t['index'][1]) +
								'<span class="tnsw0_tt" style="display:none;">' + t['tense'] + '</span>' +
							'</span>';
				prev_match_indx = t['index'][1];
				word_counter += 1;
			}
			new_sen += page_j[s_num].substring(prev_match_indx);
			page_j[s_num] = new_sen;
			gl_page_container_obj.innerHTML = json_to_flat(page_j, true);
		}
	}
}

function mov_tt(word_cl){
	var word = document.querySelector('.' + word_cl);
	var word_tt = word.querySelector('.tnsw0_tt');
	word_tt.style.display = 'block';
	word_tt.style.left = - (word_tt.offsetWidth - word.offsetWidth) / 2 + 'px';
	word_tt.style.opacity = '1';
}

function mou_tt(word_cl){
	var word = document.querySelector('.' + word_cl);
	var word_tt = word.querySelector('.tnsw0_tt');
	word_tt.style.opacity = '0';
	setTimeout(function(){word_tt.style.display = 'none';},200);
}

function getRandomColor() {
	var letters = '56789ABCDEF';
	var color = '#';
	for (var i = 0; i < 6; i++) {
		color += letters[Math.floor(Math.random() * 11)];
	}
	return color;
}


function json_to_flat(json_page, with_sen = false) {
	res = '<p>';
	is_in_parag = true;
	for (var key in json_page) {
		if (json_page.hasOwnProperty(key)) {
			if (json_page[key].substring(0, 2) == "\n\n") {
				if (is_in_parag) {
					res += '</p><p>';
				} else {
					is_in_parag = true;
					res += '<p>';
				}
			}
			ex_class = '';
			if (with_sen && json_page[key].search('tnsw0') == -1) {
				ex_class = ' class="page_word" onclick="click_page_sen(\'s' + key + '\')" '
			}
			res += '<span name="s' + key + '"' + ex_class + '>' + json_page[key].trim().replace('\n\n', '<br>') + '.</span>';
		}
	}
	if (is_in_parag) {
		res += '</p>';
	}
	return res;
}