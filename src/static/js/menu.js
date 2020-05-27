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