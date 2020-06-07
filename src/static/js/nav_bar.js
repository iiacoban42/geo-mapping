/* Open when someone clicks on the span element */
function openNav() {
    document.getElementById("open").style.visibility = "hidden";
    document.getElementById("myNav").style.width = "10%";

}

/* Close when someone clicks on the "x" symbol inside the overlay */
function closeNav() {
    document.getElementById("open").style.visibility = "visible";
    document.getElementById("myNav").style.width = "0%";
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