var MAX_SELECTED = parseInt(document.getElementById('max_reserv').innerHTML)
var selected = 0;
var but = document.getElementById('submit')

function reset_checkboxes() {
    var inputs = document.getElementsByTagName("input");
    for(var i=0; i<inputs.length; i++) {
        if (inputs[i].type === 'checkbox')
            if (inputs[i].checked)
                inputs[i].checked = false;
    }
}

function toggle_checkbox(elmnt) {
    var chkbox = elmnt.querySelector('input');
    chkbox.checked = chkbox.checked ? false : true;
}

function click_handler() {
    if (!this.classList.contains('selected')) {
        if (selected < MAX_SELECTED) {
            this.classList.toggle('selected');
            toggle_checkbox(this);
            selected++;
        }
    }
    else {
        this.classList.toggle('selected');
        toggle_checkbox(this);
        selected--;
    }
    if (selected > 0)
        but.removeAttribute('disabled');
    else but.setAttribute('disabled','');
}

function assign_click_handler() {
    all_periods = document.getElementsByClassName('time');
    for(var i=0; i<all_periods.length; i++) {
        if (!all_periods[i].classList.contains("booked"))
            all_periods[i].addEventListener("click", click_handler);
    }
}

function test() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://127.0.0.1:8000/book/?1', true);
    xhr.send();
    xhr.addEventListener("readystatechange", processRequest, false);
    function processRequest(e) {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // var resp = JSON.parse(xhr.responseText);
            alert("cool");
        }
    }
}

assign_click_handler();
reset_checkboxes();
