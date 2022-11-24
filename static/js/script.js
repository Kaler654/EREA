function getIframeSelectionText(iframe) {
    let win = iframe.contentWindow;
    let doc = iframe.contentDocument || win.document;

    if (win.getSelection) {
        let resSelection = win.getSelection().toString();
        return resSelection;
    } else if (doc.selection && doc.selection.createRange) {
        let resSelection = doc.selection.createRange().text;
        return resSelection;
    }
}

function delIframeSelection(iframe) {
    let win = iframe.contentWindow;
    let doc = iframe.contentDocument || win.document;
    if (win.getSelection) {
        win.getSelection().removeAllRanges();
    } else if (doc.selection && doc.selection.createRange) {
        win.getSelection().removeAllRanges();
    }
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
                let htmlModal = '<div class="modal__translate"><span class="word_tat">tat_word</span> — <span class="word_ru">ru_word</span></div>'.replace("tat_word", selectedText).replace("ru_word", translate) +
                    '<span class="modal__btn" onclick="addWordToDictionary()">Добавить в словарик</span>';
                new ModalWindow(htmlModal).show();
                delIframeSelection(document.querySelectorAll("iframe")[0])
                console.log("onreadystatechange")
            }
        }
        ;
    };
    console.log("getTranslate`")
}


function startSelect() {
    console.log("go");
    document.querySelectorAll("iframe")[0].contentDocument.addEventListener('mouseup', event => {
        let iframe = document.querySelectorAll("iframe")[0];
        let selectText = getIframeSelectionText(iframe);
        console.log(selectText.length)
        if ((selectText.length > 1) && (selectText.length < 200)) {
            console.log(selectText)
            console.log(selectText.length)
            if (document.querySelectorAll(".modal-window").length < 1) {
                getTranslate(selectText);
            }
        }
    });
}

function addWordToDictionary() {
    let word_tat = document.querySelectorAll(".word_tat")[0].innerHTML
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/add_wordToDict", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        word: word_tat
    }));
    document.querySelectorAll(".modal__btn")[0].innerHTML = "Удалить из словарика"
    document.querySelectorAll(".modal__btn")[0].setAttribute("onclick", "removeWordFromDictionary()")
}

function removeWordFromDictionary() {
    let word_tat = document.querySelectorAll(".word_tat")[0].innerHTML
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/remove_wordFromDict", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        word: word_tat
    }));
    document.querySelectorAll(".modal__btn")[0].innerHTML = "Добавить в словарик"
    document.querySelectorAll(".modal__btn")[0].setAttribute("onclick", "addWordToDictionary()")
}

function hang_links() {
    tocLinks = document.querySelectorAll(".toc_link")
    for (index = 0; index < tocLinks.length; index++) {
        console.log(tocLinks[index])
        tocLinks[index].setAttribute("onclick", "setTimeout(startSelect, 1000)")
    }
}


setTimeout(startSelect, 1000)
setTimeout(hang_links, 1000)

