var currentIdBook = 0;
var cardsTable = document.querySelector("#cardsTable");
// cardsTable.appendChild();

var books = 
 {
    0 : {
        "author" : "Л. Кэрролл",
        "title" : "Алиса в стране чудес",
        "img" : "/r/p14.png",
        "description" : "Писатель Льюис Кэрролл написал книгу \"Алиса в стране чудес\" в 1865 году. Алиса обычная девочка, которая скучая сидела на берегу вместе со своей сестрой, но внезапно странным образом появившийся кролик, показал ей путь в страну чудес со множеством приключений впереди.",
        "level" : "B2"
    },
    1 : {
        "author" : "О. Уайлд",
        "title" : "Портрет Дориана Грея",
        "img" : "/r/p15.png",
        "description" : "Писатель Оскар Уайлд написал книгу \"Портрет Дориана Грея\"  в 1890 году. Дориан Грей - красивый молодой человек, который решил посвятить свою жизнь гедонизму и наслаждению, и утопает в разврате. Действия Дориана приводят его к достаточно трегическим последствиям, ведь всему есть своя цена.",
        "level" : "С2"
    },
    2 : {
        "author" : "Г. Х. Андерсен",
        "title" : "Русалочка",
        "img" : "/r/p16.png",
        "description" : "Писатель Ганс Христиан Андерсен написал книгу \"Русалочка\"  в 1837 году.  История Русалочки - самой младшей из дочерей короля подводного мира, которая однажды встретила свою настоящую любовь на поверхности моря, и была готова ради нее на все.",
        "level" : "B1"
    },
    3 : {
        "author" : "Л. Кэрролл",
        "title" : "Алиса в стране чудес",
        "img" : "/r/p14.png",
        "description" : "Писатель Льюис Кэрролл написал книгу \"Алиса в стране чудес\" в 1865 году. Алиса обычная девочка, которая скучая сидела на берегу вместе со своей сестрой, но внезапно странным образом появившийся кролик, показал ей путь в страну чудес со множеством приключений впереди.",
        "level" : "B2"
    },
    4 : {
        "author" : "О. Уайлд",
        "title" : "Портрет Дориана Грея",
        "img" : "/r/p15.png",
        "description" : "Писатель Оскар Уайлд написал книгу \"Портрет Дориана Грея\"  в 1890 году. Дориан Грей - красивый молодой человек, который решил посвятить свою жизнь гедонизму и наслаждению, и утопает в разврате. Действия Дориана приводят его к достаточно трегическим последствиям, ведь всему есть своя цена.",
        "level" : "С2"
    },
    5 : {
        "author" : "Г. Х. Андерсен",
        "title" : "Русалочка",
        "img" : "/r/p16.png",
        "description" : "Писатель Ганс Христиан Андерсен написал книгу \"Русалочка\"  в 1837 году.  История Русалочки - самой младшей из дочерей короля подводного мира, которая однажды встретила свою настоящую любовь на поверхности моря, и была готова ради нее на все.",
        "level" : "B1"
    },
    6 : {
        "author" : "Л. Кэрролл",
        "title" : "Алиса в стране чудес",
        "img" : "/r/p14.png",
        "description" : "Писатель Льюис Кэрролл написал книгу \"Алиса в стране чудес\" в 1865 году. Алиса обычная девочка, которая скучая сидела на берегу вместе со своей сестрой, но внезапно странным образом появившийся кролик, показал ей путь в страну чудес со множеством приключений впереди.",
        "level" : "B2"
    },
    7 : {
        "author" : "О. Уайлд",
        "title" : "Портрет Дориана Грея",
        "img" : "/r/p15.png",
        "description" : "Писатель Оскар Уайлд написал книгу \"Портрет Дориана Грея\"  в 1890 году. Дориан Грей - красивый молодой человек, который решил посвятить свою жизнь гедонизму и наслаждению, и утопает в разврате. Действия Дориана приводят его к достаточно трегическим последствиям, ведь всему есть своя цена.",
        "level" : "С2"
    },
    8 : {
        "author" : "Г. Х. Андерсен",
        "title" : "Русалочка",
        "img" : "/r/p16.png",
        "description" : "Писатель Ганс Христиан Андерсен написал книгу \"Русалочка\"  в 1837 году.  История Русалочки - самой младшей из дочерей короля подводного мира, которая однажды встретила свою настоящую любовь на поверхности моря, и была готова ради нее на все.",
        "level" : "B1"
    }
};

function downloadCard() {
    for (let i = 0; i < 8; ++i) {
        createCard();
    }
}

function createCard() {
    var col = document.createElement('col');

    var card = document.createElement('div');
    card.className = 'card';
    card.dataset.bsWhatever = `${currentIdBook}`;
    card.dataset.bsToggle = "modal";
    card.dataset.bsTarget = "#exampleModal";
    col.appendChild(card);

    var author = document.createElement('span');
    author.className = 'authorCard';
    author.innerHTML = books[currentIdBook]["author"];
    card.appendChild(author);

    var cardBody = document.createElement('div');
    cardBody.className = 'card';
    card.appendChild(cardBody);

    var img = document.createElement('img');
    img.className = 'card-img-top cardImg';
    img.src = books[currentIdBook]["img"];
    cardBody.appendChild(img);

    var title = document.createElement('span');
    title.className = 'titleCard';
    title.innerHTML = books[currentIdBook]["title"];
    card.appendChild(title);

    cardsTable.appendChild(col);

    currentIdBook++;
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