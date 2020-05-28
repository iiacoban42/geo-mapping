var map;
require(["esri/map", "esri/layers/ArcGISTiledMapServiceLayer", "dojo/domReady!"],
    function (Map, Tiled) {
        map = new Map("map", {
            center: [-122.45, 37.75],
        });
        var tiled = new Tiled("https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_2016/MapServer");
        map.addLayer(tiled);
    }
);

function changeYear(year) {
    console.log(year)
    var baseMapLayer = new esri.layers.ArcGISTiledMapServiceLayer("https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + year + "/MapServer");
    map.removeAllLayers();
    map.addLayer(baseMapLayer);
}

/* Open when someone clicks on the span element */
function openNav() {
    document.getElementById("open").style.visibility = "hidden";
    document.getElementById("myNav").style.width = "7%";

}

/* Close when someone clicks on the "x" symbol inside the overlay */
function closeNav() {
    document.getElementById("open").style.visibility = "visible";
    document.getElementById("myNav").style.width = "0%";
}

var btn_captcha = document.getElementById('captcha');
btn_captcha.onclick = function () {
    console.log("captcha")
    location.assign('/captcha/');
}

var btn_overview = document.getElementById('overview');
btn_overview.onclick = function () {
    console.log("tiles_overview")
    location.assign('/tiles_overview/');
}

$(document).ready(function () {
    $(menu).click(function (event) {
        if (event.target.id !== 'menu') {
            changeYear(event.target.id);
            document.getElementById("current").innerHTML = event.target.id;
        }
    });
});