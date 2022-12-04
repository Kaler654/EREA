// Анимация при прокрутке

const animItems = document.querySelectorAll('._anim-items');

if (animItems.length > 0) {
    window.addEventListener('scroll', animOnScroll);

    function animOnScroll() {
        for (let index = 0; index < animItems.length; index++) {
            const animItem = animItems[index];
            const animItemHeight = animItem.offsetHeight;
            const animItemOffset = offset(animItem).top;
            const animStart = 4;

            let animItemPoint = window.innerHeight - animItemHeight / animStart;
            if (animItemHeight > window.innerHeight) {
                animItemPoint = window.innerHeight - window.innerHeight / animStart;
            }

            if ((pageYOffset > animItemOffset - animItemPoint + 80) && pageYOffset < (animItemOffset + animItemHeight)) {
                animItem.classList.add('_active');
            } else {
                if (!animItem.classList.contains('_anim-no-hide')) {
                    animItem.classList.remove('_active');
                }
            }
        }
    }


    function offset(el) {
        const rect = el.getBoundingClientRect(),
            scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
            scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        return {top: rect.top + scrollTop, left: rect.left + scrollLeft}
    }

    setTimeout(() => {
        animOnScroll();
    }, 300);
}

function getTranslate(selectedText) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/get_translate", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        text: selectedText
    }));

    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            let data = JSON.parse(this.responseText);
            let translate = data["translate"];
            if (document.querySelectorAll(".modal-window").length < 1) {
                let htmlModal = '<div class="modal__translate"><span class="word_en">tat_word</span> — <span class="word_ru">ru_word</span></div>'.replace("tat_word", selectedText).replace("ru_word", translate) +
                    '<span class="modal__btn" onclick="addWordToDictionary()">Добавить в словарик</span>';
                new ModalWindow(htmlModal).show();
                console.log("onreadystatechange")
                iframe = document.querySelectorAll("iframe")[0].contentWindow;
                iframe.getSelection().removeAllRanges()
            }
        }
        ;
    };
    console.log("getTranslate`")
}

function addWordToDictionary() {
    let word_en = document.querySelectorAll(".word_en")[0].innerHTML
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/add_wordToDict", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        word: word_en
    }));
    document.querySelectorAll(".modal__btn")[0].innerHTML = "Удалить из словарика"
    document.querySelectorAll(".modal__btn")[0].setAttribute("onclick", "removeWordFromDictionary()")
}

function removeWordFromDictionary() {
    let word_en = document.querySelectorAll(".word_en")[0].innerHTML
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/remove_wordFromDict", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        word: word_en
    }));
    document.querySelectorAll(".modal__btn")[0].innerHTML = "Добавить в словарик"
    document.querySelectorAll(".modal__btn")[0].setAttribute("onclick", "addWordToDictionary()")
}


// setTimeout(startSelect, 1000)
