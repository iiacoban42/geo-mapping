var map;
require(["esri/Map", "esri/WebMap", "esri/views/MapView", "esri/layers/TileLayer", "esri/layers/FeatureLayer", "dojo/domReady!"],
    function (Map, WebMap, MapView, TileLayer, FeatureLayer) {
        var baseLayer = new TileLayer({
            url: "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_2016/MapServer"
        });
        map = new Map("map", {
            center: [-122.45, 37.75],
        });
        map.add(baseLayer)
        var buildingsLayer = new FeatureLayer({
            url: "https://services.arcgis.com/V6ZHFr6zdgNZuVG0/ArcGIS/rest/services/netherlands/FeatureServer/9",
            outFields: ["*"]
        });
        map.add(buildingsLayer);
        var view = new MapView({
            container: "map",
            map: map
        });

        $(document).ready(function () {
                $(menu).click(function (event) {
                    if (event.target.id !== 'menu') {
                        var year = event.target.id
                        console.log(year)
                        var yearLayer = new TileLayer({
                            url: "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + year + "/MapServer"
                        });
                        map.removeAll();
                        map.add(yearLayer);
                        document.getElementById("current").innerHTML = event.target.id;
                    }
                });
            }
        );
    });

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
