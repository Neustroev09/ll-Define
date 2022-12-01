var books = 
 {
    0 : {
        "author" : "Л. Кэрролл",
        "title" : "Алиса в стране чудес",
        "img" : "/r/p14.png",
        "description" : "Писатель Льюис Кэрролл написал книгу \"Алиса в стране чудес\" в 1865 году. Алиса обычная девочка, которая скучая сидела на берегу вместе со своей сестрой, но внезапно странным образом появившийся кролик, показал ей путь в страну чудес со множеством приключений впереди.",
        "difficulty" : "B2",
        "genre" : "Фантастика"
    },
    1 : {
        "author" : "О. Уайлд",
        "title" : "Портрет Дориана Грея",
        "img" : "/r/p15.png",
        "description" : "Писатель Оскар Уайлд написал книгу \"Портрет Дориана Грея\" в 1890 году. Дориан Грей - красивый молодой человек, который решил посвятить свою жизнь гедонизму и наслаждению, и утопает в разврате. Действия Дориана приводят его к достаточно трегическим последствиям, ведь всему есть своя цена.",
        "difficulty" : "C2",
        "genre" : "Фантастика"
    },
    2 : {
        "author" : "Г. Х. Андерсен",
        "title" : "Русалочка",
        "img" : "/r/p16.png",
        "description" : "Писатель Ганс Христиан Андерсен написал книгу \"Русалочка\" в 1837 году.  История Русалочки - самой младшей из дочерей короля подводного мира, которая однажды встретила свою настоящую любовь на поверхности моря, и была готова ради нее на все.",
        "difficulty" : "B1",
        "genre" : "Сказка" 
    },
    3 : {
        "author" : "Б. Гримм",
        "title" : "Рапунцель",
        "img" : "/r/p17.png",
        "description" : "Писатель Братья Гримм написал книгу \"Рапунцель\" в 1812 году. Сказка о паре молодых людей, которая не имела ребенка, но всегда о нем мечтала, и поэтому обратившаяся к колдунье.",
        "difficulty" : "A1",
        "genre" : "Сказка"
    },
    4 : {
        "author" : "В. Гауфф",
        "title" : "История о корабле призраке",
        "img" : "/r/p18.png",
        "description" : "Писатель Вильгельм Гауфф написал книгу \"История о корабле призраке\" в 1890 году. История молодого человека, отправившегося в путешествия, и нашедшего корабль, вся команда и капитан которого - проклята, и обречена на вечные скитания и муки, в бесконечных морских водах.",
        "difficulty" : "A2",
        "genre" : "Ужасы"
    },
    5 : {
        "author" : "Л. Ф. Баум",
        "title" : "Волшебник страны Оз",
        "img" : "/r/p19.png",
        "description" : "Писатель Франк Баум написал книгу \"Волшебник страны Оз\" в 1900 году.  Сказка \"Волшебник страны Оз\" повествует нам историю девочки Дороти, которую унесло ураганом вместе с ее собачкой и домом и она оказалась в стране Оз. Дом упал на злую волшебницу и убил ее, чему былии рады жители страны - жевуны. Девочка обратилась за помощью к доброй волшебнице, чтобы она помогал ей вернуться домой и та направила ее к волшебнику Озу.",
        "difficulty" : "A2",
        "genre" : "Приключения" 
    },
    6 : {
        "author" : "Д. Дефо",
        "title" : "Робинзон Крузо",
        "img" : "/r/p20.png",
        "description" : "Писатель Даниэль Дефо написал книгу \"Робинзон Крузо\" в 1719 году. Робинзон Крузо всегда мечтал о путешествиях в другие земли, чего он и добился вопреки воли его отца. После кораблекрушения возле неизвестного необитаемого острова, в котором единственным выжившим оказался лишь он, находит силы и собирает всевозможные уцелевшие вещи, чтобы выжить и обосноваться на острове.",
        "difficulty" : "C1",
        "genre" : "Приключения"
    },
    7 : {
        "author" : "Б. Гримм",
        "title" : "Ганзель и Гретель",
        "img" : "/r/p21.png",
        "description" : "Писатель Братья Гримм написал книгу \"Ганзель и Гретель\" в 1812 году. Гензель и Гретель - брат и сестра, брошенные отцом и мачехой в лесу. Пытаясь выбраться из леса они попадают в руки ведьмы, которая живет в доме из имбирных пряников, торта и пирожных.",
        "difficulty" : "A1",
        "genre" : "Сказка"
    },
    8 : {
        "author" : "Г. Лавкрафт",
        "title" : "Хребты безумия",
        "img" : "/r/p22.png",
        "description" : "Писатель Говард Лавкрафт написал книгу \"Хребты безумия\" в 1936 году. События книги разворачиваются в далеких снегах Антарктики, где во время одной из экспедиций, ученые обнаруживают останки древнего города, в течение миллионов лет погребенного под огромной толщей льда...",
        "difficulty" : "C1",
        "genre" : "Ужасы" 
    }
};

var maxCountBooksInPage = 8;

function downloadCard(numberPage=0) {
    for (let i = 0; i < maxCountBooksInPage; ++i) {
        createCard(i);
    }

    if (document.documentElement.scrollWidth < 1000) {
        document.querySelector(".filterBlock").style.display = 'none';
        document.querySelector(".btnOffCanvas").style.display = '';
    } else {
        document.querySelector(".filterBlock").style.display = '';
        document.querySelector(".btnOffCanvas").style.display = 'none';
    }
}

function updateCard(booksId) {
    if (!booksId.length) {
        clearCard();
        var cardsTable = document.querySelector("#cardsTable");
        var label = document.createElement('div');
        label.className = 'filterTitle';
        label.innerHTML = 'Ничего не найдено'
        label.style = 'margin-top: 25%; margin-bottom: 25%; text-align: center;';
        cardsTable.appendChild(label);
    } else {
        clearCard();
        for (let i = 0; i < booksId.length; ++i) {
            /// Поправить при добавлении нескольких страниц
            if (i >= maxCountBooksInPage) {
                break;
            }
            createCard(booksId[i]);
        }
    }
}

function clearCard() {
    document.querySelector("#cardsTable").innerHTML = "";
}

function createCard(id) {
    var col = document.createElement('col');

    var card = document.createElement('div');
    card.className = 'card';
    card.dataset.bsWhatever = `${id}`;
    card.dataset.bsToggle = "modal";
    card.dataset.bsTarget = "#exampleModal";
    col.appendChild(card);

    var author = document.createElement('span');
    author.className = 'authorCard';
    author.innerHTML = books[id]["author"];
    card.appendChild(author);

    var cardBody = document.createElement('div');
    cardBody.className = 'card cardImgDiv';
    card.appendChild(cardBody);

    var img = document.createElement('img');
    img.className = 'card-img-top cardImg';
    img.src = books[id]["img"];
    cardBody.appendChild(img);

    var title = document.createElement('span');
    title.className = 'titleCard';
    title.innerHTML = books[id]["title"];
    card.appendChild(title);

    var cardsTable = document.querySelector("#cardsTable");
    cardsTable.appendChild(col);
}

function descriptionCard(event) {
    var bookId = event.relatedTarget.getAttribute('data-bs-whatever');
    var modalTitle = exampleModal.querySelector('#modalLabel');
    modalTitle.innerHTML = `Книга «${books[bookId]["title"]}» на английском языке`;

    var modalBody = exampleModal.querySelector('#modalBody');
    modalBody.innerHTML = `${books[bookId]["description"]}`;
}

var exampleModal = document.getElementById('exampleModal')
exampleModal.addEventListener('show.bs.modal', function (event) {
    descriptionCard(event);
})


function filter() {
    var booksId = new Array();
    var emptyPage = false;

    var nameInput = document.querySelector('.inputText').value; 
    if (nameInput != "") {
        filterByTitleAuthor(booksId, nameInput)
        emptyPage = true
    }

    /// TODO фильтр должен быть последовательным
    var checkObjList = document.querySelectorAll('#genreCheck');
    for (let i = 0; i < checkObjList.length; ++i) {
        if (checkObjList[i].checked) {
            filterCheck(booksId, checkObjList[i].value, "genre");
            emptyPage = true
        }
    }

    var checkObjList = document.querySelectorAll('#difficultyCheck');
    for (let i = 0; i < checkObjList.length; ++i) {
        if (checkObjList[i].checked) {
            filterCheck(booksId, checkObjList[i].value, "difficulty");
            emptyPage = true
        }
    }

    if (!emptyPage) {
        clearCard()
        downloadCard();
    } else {
        updateCard(booksId);
    }
   
    document.getElementById('btnCloseOff').click();
}

function filterByTitleAuthor(booksId, nameInput) {
    nameInput = nameInput.toLowerCase()
    for (const [key, value] of Object.entries(books)) {
        if (value["author"].toLowerCase().indexOf(nameInput,0) != -1 || value["title"].toLowerCase().indexOf(nameInput,0) != -1) {
            booksId.push(key);
        }
    }
}

function filterCheck(booksId, checkValue, checkKey) {
    for (const [key, value] of Object.entries(books)) {
        if (value[checkKey] == checkValue) {
            booksId.push(key);
        }
    }
}

function crateOffCanvas() {
    var offCanvasBody = document.querySelector(".offcanvas-body");
    offCanvasBody.innerHTML = '';
    
    var filterBlock = document.querySelector(".filterBlock");
    var cloneBlock = filterBlock.cloneNode(true);
    cloneBlock.style.display = '';
    cloneBlock.className = 'filterBlockOff';
    offCanvasBody.appendChild(cloneBlock);    
}

window.addEventListener('resize', function(event) {
    if (document.documentElement.scrollWidth < 1000) {
        document.querySelector(".filterBlock").style.display = 'none';
        document.querySelector(".btnOffCanvas").style.display = '';
    } else {
        document.querySelector(".filterBlock").style.display = '';
        document.querySelector(".btnOffCanvas").style.display = 'none';
    }
}, true);