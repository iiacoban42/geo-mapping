var map;
var view;
require(["esri/Map", "esri/views/MapView", "esri/layers/TileLayer", "esri/Graphic", "esri/PopupTemplate", "dojo/domReady!"],
    function (Map, MapView, TileLayer, Graphic, PopupTemplate) {
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

        labels = text.labels
        points = text.points
        for (let i = 0; i < points.length; i++) {
            var pointGraphic = new Graphic({geometry: points[i], symbol: pointSymbol, attributes: labels[i]});
            pointGraphic.popupTemplate = template
            view.graphics.add(pointGraphic);

        }


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


// sorry
var text = {
    "labels": [
        {
            "Label": "Label",
            "Name": "Mali",
            "Other": "-"
        },
        {
            "Label": "Label",
            "Name": "Paula",
            "Other": "-"
        },
        {
            "Label": "Label",
            "Name": "Andrei",
            "Other": "-"
        },
        {
            "Label": "Label",
            "Name": "Georgi",
            "Other": "-"
        },
        {
            "Label": "Label",
            "Name": "Boris",
            "Other": "-"
        }
    ],
    "points": [
        {
            "type": "point",
            "longitude": "4.470590",
            "latitude": "51.922910"
        },
        {
            "type": "point",
            "longitude": "4.300700",
            "latitude": "52.070499"
        },
        {
            "type": "point",
            "longitude": "4.357068",
            "latitude": "52.011578"
        },
        {
            "type": "point",
            "longitude": "-355.269549",
            "latitude": "51.767840"
        },
        {
            "type": "point",
            "longitude": "-355.187097",
            "latitude": "52.116626"
        }
    ]
}