$(document).ready(function () {
    document.onclick = function (e) {
        let elem = e.target.parentElement.id
        let menu = document.getElementById('myNav')
        if (elem === 'nav' && menu.style.width < '5%')
            openNav();
        else if (menu.style.width >= '5%')
            closeNav();
    };
});

// open when someone clicks on the span element
function openNav() {
    document.getElementById('open').classList.replace("fa-bars", "fa-times")
    document.getElementById('myNav').style.width = '5%';
}

// close when someone clicks on the 'x' symbol inside the overlay
function closeNav() {
    document.getElementById('open').classList.replace("fa-times", "fa-bars")
    document.getElementById('myNav').style.width = '0%';

}

$(document).ready(function () {
    $(menu).click(function (event) {
        console.log(event.target.id);
        if (event.target.id === 'maps')
            location.assign('/');
        else if (event.target.id === 'menu')
            return
        else
            location.assign('/' + event.target.id + '/');
    });
});