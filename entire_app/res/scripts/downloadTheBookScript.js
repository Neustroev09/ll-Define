var valid_file_types = ['text/plain', 'application/pdf'],
	valid_file_types_mess = ['TXT', 'PDF'];

var real_button = document.querySelector("#bt-select-book"),
	pseudo_button = document.querySelector("#_bt-file-selector"),
	file_info = document.querySelector("#user-file-info span"),
	file_form = document.querySelector("#_fm_loadbook"),
	load_button = document.querySelector("#bt-load-book");

var pseudo_button_click = () => pseudo_button.click();
real_button.addEventListener('click', pseudo_button_click);

function file_change_event() {
	var files = pseudo_button.files;

	if (files.length == 0) {
		file_info.textContent = "Нажмите на «Выбрать книгу», выбирете нужный файл и затем нажмите на «Загрузить книгу».";
	} else {
		real_file = files[0];
		file_name = document.createElement("b");
		file_name.textContent = real_file.name
		file_info.textContent = "Выбран файл";
		file_info.appendChild(document.createElement("br"));
		file_info.appendChild(file_name);
		file_info.appendChild(document.createElement("br"));
		file_type_info = document.createElement('span');
		file_type_info.textContent = "Тип книги: "
		var type_index = get_valid_file_mess(real_file.type);
		if (type_index != -1) {
			file_type_info.textContent += valid_file_types_mess[type_index] + " книга";
		} else {
			file_type_info.textContent += "неизвестный формат";
		}
		file_info.appendChild(file_type_info);
		file_info.appendChild(document.createElement("br"));
		file_size_info = document.createElement('span');
		file_size_info.textContent = "Размер файла: " + real_file.size / 1000. + " Кб";
		file_info.appendChild(file_size_info);
	}
}
pseudo_button.addEventListener('change', file_change_event);

function get_valid_file_mess (type) {
	return valid_file_types.findIndex((vtype) => vtype == type);
}

var pseudo_form_submit = () => file_form.submit();
load_button.addEventListener('click', pseudo_form_submit);