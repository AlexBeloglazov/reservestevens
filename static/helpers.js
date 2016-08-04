var max = document.getElementById('max_reserv');
var MAX_SELECTED = max ? parseInt(max.innerHTML) : 9999;
var selected = 0;
var but = document.querySelector('button[type="submit"]')

function reset_checkboxes() {
    var inputs = document.getElementsByTagName("input");
    for(var i=0; i<inputs.length; i++) {
        if (inputs[i].type === 'checkbox')
            if (inputs[i].checked)
                inputs[i].checked = false;
    }
}

function toggle_checkbox(elmnt) {
    var chkbox = elmnt.querySelector('.time > input');
    if (chkbox)
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
    all_periods = document.getElementsByClassName('select');
    for(var i=0; i<all_periods.length; i++) {
        if (!all_periods[i].classList.contains("booked"))
            all_periods[i].addEventListener("click", click_handler);
    }
}


assign_click_handler();
reset_checkboxes();
