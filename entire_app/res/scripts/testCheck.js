function checkAnswer() {
    var countRadioPoint = checkRadio();
    var countSelectPoint = checkSelect();
    finalCountPoints = countRadioPoint + countSelectPoint;
    localStorage.setItem("finalCountPoints", finalCountPoints);
}

function checkRadio() {
    var answer = [0,1,2,2,2,2,1,1,1,1,1,2,1,2,0,2,1,2,0,0,1,2,0,1,0,2,2,1];
    var currentAnswer = 0;
    var name;
    var countQuestion = 14;
    var countPoints = 0;
    
    for (var currentQuestion = 1; currentQuestion <= countQuestion; ++currentQuestion) {
        name = `input[name="question${currentQuestion}Radio"]`;
        var selected = document.querySelectorAll(name);
        if (selected.length == 0) {
            for (var currentSubnubnumberQuestion = 1; currentSubnubnumberQuestion <= 15; ++currentSubnubnumberQuestion) {
                name = `input[name="question${currentQuestion}_${currentSubnubnumberQuestion}Radio"]`;
                selected = document.querySelectorAll(name);
                if (selected.length != 0) {
                    var count = 0;
                    flagCheck = false;
                    for (radioButton of selected) {
                        if (radioButton.checked && count == answer[currentAnswer]) {
                            countPoints++;
                            radioButton.style["boxShadow"] = "0 0 5px 0.1rem #0bee44";
                            flagCheck = true;
                            break;
                        } 
                        if (radioButton.checked && count != answer[currentAnswer]) {
                            radioButton.style["boxShadow"] = "0 0 5px 0.1rem #df120b";
                            flagCheck = true
                            break;
                        }
                        count++;
                    }
                    if (!flagCheck) {
                        for (radioButton of selected) {
                            radioButton.style["boxShadow"] = "0 0 5px 0.1rem #df120b";
                        }
                    }
                    currentAnswer++;
                } else  
                    break;
            }
        } else {
            if (selected.length != 0) {
                var count = 0;
                flagCheck = false;
                for (radioButton of selected) {
                    if (radioButton.checked && count == answer[currentAnswer]) {
                        countPoints++;
                        radioButton.style["boxShadow"] = "0 0 5px 0.1rem #0bee44";
                        flagCheck = true;
                        break;
                    } 
                    if (radioButton.checked && count != answer[currentAnswer]) {
                        radioButton.style["boxShadow"] = "0 0 5px 0.1rem #df120b";
                        flagCheck = true;
                        break;
                    }
                    count++;
                }
                if (!flagCheck) {
                    for (radioButton of selected) {
                        radioButton.style["boxShadow"] = "0 0 5px 0.1rem #df120b";
                    }
                }
                currentAnswer++;
            } else {
                continue;
            }
        }
    }
    return countPoints;
}

function checkSelect() {
    var answer = [2,1,1,1,1,2,4,4,3,2,2,2];
    var currentAnswer = 0;
    var idName;
    var countQuestion = 14;
    var countPoints = 0;
    
    for (var currentQuestion = 1; currentQuestion <= countQuestion; ++currentQuestion) {
        idName = `questionSelect${currentQuestion}`;
        var selected = document.getElementById(idName);
        if (selected === null) {
            for (var currentSubnubnumberQuestion = 1; currentSubnubnumberQuestion <= 4; ++currentSubnubnumberQuestion) {
                idName = `questionSelect${currentQuestion}_${currentSubnubnumberQuestion}`;
                selected = document.getElementById(idName);
                if (selected !== null) {
                    if (selected.selectedIndex == answer[currentAnswer]) {
                        countPoints++;
                        currentAnswer++;
                        selected.style["boxShadow"] = "0 0 5px 0.1rem #0bee44";
                    } else {
                        currentAnswer++;
                        selected.style["boxShadow"] = "0 0 5px 0.1rem #df120b";
                    }
                } else {
                    break;
                }
            }
        } else {
            if (selected.selectedIndex == answer[currentAnswer]) {
                countPoints++;
                currentAnswer++;
                selected.style["boxShadow"] = "0 0 5px 0.1rem #0bee44";
            } else {
                currentAnswer++;
                selected.style["boxShadow"] = "0 0 5px 0.1rem #df120b";
            }
        }
    }
    return countPoints;
}

function definitionLevel() {
    var countPoints = 0;
    countPoints = localStorage.getItem("finalCountPoints");
    var yourLevel;
    var levelDescription;
    if (countPoints >= 0 && countPoints <= 10) { 
        yourLevel = 'Beginner';
        levelDescription = 'Вам знакомы азы английского языка. Скорее всего, Вы только начали изучать английский или обладаете остаточными знаниями языка со времен школы. Вы умеете читать и писать, знаете алфавит, можете представиться и сообщить самую простую информацию о себе на английском. Но Ваших знаний совершенно недостаточно для общения в типичных жизненных ситуациях. Человек с уровнем Beginner стоит в самом начале длинного и увлекательного пути к вершинам английского языка.';
    }
    if (countPoints >= 11 && countPoints <= 20) {
        yourLevel = 'Elementary (A1)'; 
        levelDescription = 'Вам знакомы азы английского языка. Скорее всего, Вы только начали изучать английский или обладаете остаточными знаниями языка со времен школы. Вы умеете читать и писать, знаете алфавит, можете представиться и сообщить самую простую информацию о себе на английском. Но Ваших знаний совершенно недостаточно для общения в типичных жизненных ситуациях. Человек с уровнем Elementary стоит в самом начале длинного и увлекательного пути к вершинам английского языка.';
    }
    if (countPoints >= 21 && countPoints <= 30) {
        yourLevel = 'Pre-Intermediate (A2)';
        levelDescription = 'Вам есть чем гордиться, но, главное, есть к чему стремиться! Часто именно после уровня Pre-Intermediate трудно сделать качественный скачок в знаниях, ведь уже можно общаться с иностранцами в медленном темпе, читать адаптированные книги, смотреть видеоподкасты, но полная свобода еще не ощущается. Вы знаете условные предложения и модальные глаголы, понимаете разницу между be going to и Future Simple, разбираетесь в типах вопросов, но эти навыки еще не доведены до автоматизма. Все это отрабатывается на следующем уровне.';
    }
    if (countPoints >= 31 && countPoints <= 36) {
        yourLevel = 'Intermediate (B1)';
        levelDescription = 'Уровень Intermediate — это довольно серьезный уровень знаний, несмотря на то, что он переводится как «средний». Сложные грамматические конструкции, чтение больших текстов, прослушивание интервью на английском уже не представляют особых трудностей для Вас. Однако Ваши знания скорее общего характера без тематического уклона. Вам знакомы слова общей тематики, которые часто используются в речи, но специфическая лексика, частные случаи употребления фразовых глаголов, многие идиомы пока неизвестны. Это задача следующих уровней.';
    }
    if (countPoints >= 37 && countPoints <= 38) {
        yourLevel = 'Upper-Intermediate (B2)';
        levelDescription = 'Запас Ваших знаний весьма значителен. Уровня Upper-Intermediate достаточно, чтобы учиться за границей в англоязычном университете или найти работу в англоговорящей среде. Вы знакомы с самым разнообразным грамматическим материалом, способны читать и воспринимать на слух неадаптированные тексты и интервью, а самое главное — можете относительно свободно изъясняться на письменном и устном английском. Однако на данном уровне нельзя останавливаться, ведь знания имеют плохую привычку забываться. И поднявшись на такие вершины в английском, Вам будет очень обидно, если знания языка начнут пропадать.';
    }
    if (countPoints >= 39 && countPoints <= 40) {
        yourLevel = 'Advanced (C1)';
        levelDescription = 'Английский давно стал Вам верным другом, иначе такого впечатляющего уровня знаний не достичь. Вы способны читать неадаптированную художественную литературу, смотреть фильмы в оригинале, писать сочинения и письма в разных стилях и жанрах, свободно общаться с носителями языка на самые разнообразные темы. Для Вас английский — это как прочитанная книга, в которой, конечно, всегда найдется что-то новенькое, но весь сюжет и мотив ее наперед известен.';
    }
    
    var yourLevelDoc = document.getElementById('yourLevel').textContent;
    document.getElementById('yourLevel').innerText = yourLevelDoc.replace('#Level', yourLevel);

    var numberPointsDoc = document.getElementById('numberPoints').textContent;
    document.getElementById('numberPoints').innerText = numberPointsDoc.replace('#Result', countPoints);

    document.getElementById('levelDescription').innerText = levelDescription;   
}