var map;
var view;
require(["esri/Map", "esri/views/MapView", "esri/layers/TileLayer", "esri/Graphic", "dojo/domReady!"],
    function (Map, MapView, TileLayer, Graphic) {

        // initial map
        var baseLayer = new TileLayer({
            url: "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_2016/MapServer"
        });
        map = new Map("map", {
            center: [-122.45, 37.75],
        });

        map.add(baseLayer)

        // map is added to the view
        view = new MapView({
            container: "map",
            map: map,
        });


        // create a symbol for drawing the point
        var pointSymbol = {
            type: "simple-marker",             // autocasts as new SimpleMarkerSymbol()
            color: [226, 119, 40],
            width: 8,
            outline: {
                color: [255, 255, 255],
                width: 4
            }
        };

        // template for points on map
        var template = {
            title: "{Label}",
            content: [
                {
                    type: "fields",
                    fieldInfos: [
                        {
                            fieldName: "Name"
                        },
                        {
                            fieldName: "Other"
                        }
                    ]
                }
            ]
        };

        // get json with points
        document.onreadystatechange = async function () {
            const response = await fetch('/get_markers');
            const json = await response.json();
            text = JSON.parse(json)
            var labels = text.labels
            var points = text.points
            // display points in view
            for (let i = 0; i < points.length; i++) {
                var pointGraphic = new Graphic({geometry: points[i], symbol: pointSymbol, attributes: labels[i]});
                pointGraphic.popupTemplate = template
                view.graphics.add(pointGraphic);
            }
        }

        // add div element to show coords
        var coordsWidget = document.createElement("div");
        coordsWidget.id = "coordsWidget";
        coordsWidget.className = "esri-widget esri-component";
        coordsWidget.style.padding = "7px 15px 5px";
        view.ui.add(coordsWidget, "bottom-right");

        // update lat, lon, zoom and scale
        // lat and lon are in other coord system for now (hopefully)
        function showCoordinates(event) {
            var coords = "Lat/Lon (wrong for now?) " + event.y + " " + event.x +
                " | Scale 1:" + Math.round(view.scale * 1) / 1 +
                " | Zoom " + view.zoom;
            coordsWidget.innerHTML = coords;
        }

        // add event and show center coordinates after the view is finished moving e.g. zoom, pan
        view.watch(["stationary"], function () {
            showCoordinates(view.center);
        });

        // add event to show mouse coordinates on click and move
        view.on(["pointer-down", "pointer-move"], function (evt) {
            showCoordinates(view.toMap({x: evt.x, y: evt.y}));
        });


        // change years based on the selection from the menu
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

// open when someone clicks on the span element
function openNav() {
    document.getElementById("open").style.visibility = "hidden";
    document.getElementById("myNav").style.width = "7%";

}

// close when someone clicks on the "x" symbol inside the overlay
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

