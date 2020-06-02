var map;
var view;
require(["esri/Map", "esri/views/MapView", "esri/layers/TileLayer", "esri/Graphic", "dojo/domReady!"],
    function (Map, MapView, TileLayer, Graphic) {
        var baseLayer = new TileLayer({
            url: "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_2016/MapServer"
        });
        map = new Map("map", {
            center: [-122.45, 37.75],
        });
        map.add(baseLayer)

        view = new MapView({
            container: "map",
            map: map
        });

        // First create a point geometry
        var point = {
            type: "point",                     // autocasts as new Point()
            longitude: 4.470590,
            latitude: 51.922910
        };

        // Create a symbol for drawing the point
        var pointSymbol = {
            type: "simple-marker",             // autocasts as new SimpleMarkerSymbol()
            color: [226, 119, 40],
            width: 8,
            outline: {
                color: [255, 255, 255],
                width: 4
            }
        };

        // Create an object for storing attributes related to the point
        var pointLabels = {
            Name: "Mali",
            Where: "Rotterdam",
        };

        var pointGraphic = new Graphic({
            geometry: point,
            symbol: pointSymbol,
            attributes: pointLabels,
            popupTemplate: {
                title: "{Name}",
                content: [
                    {
                        type: "fields",
                        fieldInfos: [
                            {
                                fieldName: "Name"
                            },
                            {
                                fieldName: "Where"
                            }
                        ]
                    }
                ]
            }
        });

        // Add the line graphic to the view's GraphicsLayer
        view.graphics.add(pointGraphic);

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
    }
);

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
