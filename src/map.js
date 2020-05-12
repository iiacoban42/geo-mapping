var map;

require(["esri/map", "esri/layers/ArcGISTiledMapServiceLayer", "dojo/domReady!"],
    function (Map, Tiled) {
        map = new Map("map", {
            center: [-122.45, 37.75],
        });
        var tiled = new Tiled("https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_2005/MapServer");
        map.addLayer(tiled);
    }
);

function changeYear(year) {
    console.log(year)
    var baseMapLayer = new esri.layers.ArcGISTiledMapServiceLayer("https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + year + "/MapServer");
    map.addLayer(baseMapLayer);
}

/* Open when someone clicks on the span element */
function openNav() {
    document.getElementById("myNav").style.width = "25%";
}

/* Close when someone clicks on the "x" symbol inside the overlay */
function closeNav() {
    document.getElementById("myNav").style.width = "0%";
}
