var map;
var view;
var graphics = [];

require(["esri/Map", "esri/views/MapView", "esri/layers/TileLayer", "esri/Graphic", 'esri/geometry/Extent',
        'esri/widgets/Search', "esri/geometry/Circle", "dojo/domReady!"],
    function (Map, MapView, TileLayer, Graphic, Extent, Search, Circle) {

        // initial map
        var layer = new TileLayer({
            url: 'https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_2016/MapServer'
        });
        map = new Map('map', {
            center: [-122.45, 37.75],
        });

        map.add(layer)

        // map is added to the view
        view = new MapView({
            container: 'map',
            map: map,
        });

        var symbol_building = {
            type: "simple-fill",  // autocasts as new SimpleFillSymbol()
            color: [130, 130, 130, 0.3],
            style: "solid",
            outline: {  // autocasts as new SimpleLineSymbol()
                color: [130, 130, 130, 0.5],
                width: 10
            }
        };

        var symbol_land = {
            type: "simple-fill",
            color: [227, 197, 89, 0.3],
            style: "solid",
            outline: {
                color: [227, 197, 89, 0.5],
                width: 5
            }
        };

        var symbol_water = {
            type: "simple-fill",
            color: [10, 10, 204, 0.3],
            style: "solid",
            outline: {
                color: [10, 10, 204, 0.5],
                width: 2
            }
        };


        // get json with points
        // document.onreadystatechange = load_labels()
        $(predictions).click(async function (event) {
            let label = event.target.id
            document.getElementById(label).innerHTML = "loading..."
            let year = document.getElementById('current').innerHTML
            const req = {"year": year, "label": label}
            const response = await fetch('/get_all_labels/' + JSON.stringify(req));
            console.log("response")
            var json = await response.json()

            console.log(json.length)

            // display points in view
            for (let i = 0; i < json.length; i++) {
                var circleGeometry = new Circle([json[i].x_coord, json[i].y_coord], {
                    radius: 203,
                    radiusUnit: "meters",
                    spatialReference: {wkid: 28992},
                    geodesic: true
                });
                console.log(json[i].x_coord + " " + json[i].y_coord)

                if (label == "building")
                    view.graphics.add(new Graphic({geometry: circleGeometry.extent, symbol: symbol_building}));
                if (label == "land")
                    view.graphics.add(new Graphic({geometry: circleGeometry.extent, symbol: symbol_land}));

                if (label == "water")
                    view.graphics.add(new Graphic({geometry: circleGeometry.extent, symbol: symbol_water}));
                document.getElementById(label).innerHTML = label
            }
            console.log("DONE")

        });

        var coordsWidget = document.createElement('div');
        coordsWidget.id = 'coordsWidget';
        coordsWidget.className = 'esri-widget esri-component';
        coordsWidget.style.padding = '7px 15px 5px';
        view.ui.add(coordsWidget, 'bottom-right');

        // update lat, lon, zoom and scale
        // lat and lon are in other coord system for now (hopefully)
        function showCoordinates(event) {
            var coords = 'Lat/Lon (wrong for now?) ' + event.y + ' ' + event.x +
                ' | Scale 1:' + Math.round(view.scale * 1) / 1 +
                ' | Zoom ' + view.zoom;
            coordsWidget.innerHTML = coords;
        }

        // add event and show center coordinates after the view is finished moving e.g. zoom, pan
        view.watch(['stationary'], function () {
            showCoordinates(view.center);
        });

        // add event to show mouse coordinates on click and move
        view.on(['pointer-down'], function (evt) {
            showCoordinates(view.toMap({x: evt.x, y: evt.y}));
        });


        // view.on('click', function (event) {
        //     event.stopPropagation(); // overwrite default click-for-popup behavior
        //     // Get the coordinates of the click on the view
        //     year = document.getElementById('current').innerHTML
        //     coord_x_db = Math.round((event.mapPoint.x + 30527385.66843) / 406.55828)
        //     coord_y_db = Math.round((event.mapPoint.y - 31113121.21698) / (-406.41038))
        //     const req = {'year': year, 'x_coord': coord_x_db, 'y_coord': coord_y_db}
        //
        // });
        var searchWidget = new Search({view: view});
        view.ui.add(searchWidget, 'top-right');


        // change years based on the selection from the menu
        $(document).ready(function () {
                $(menu).click(function (event) {
                    if (event.target.id !== 'menu') {
                        var year = event.target.id
                        var yearLayer = new TileLayer({
                            url: 'https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_' + year + '/MapServer'
                        });
                        map.removeAll();
                        map.add(yearLayer);
                        document.getElementById('current').innerHTML = event.target.id;
                    }
                });
            }
        );
    }
);


// open when someone clicks on the span element
function openNav() {
    document.getElementById('open').style.visibility = 'hidden';
    document.getElementById('myNav').style.width = '7%';

}

function toggle_graphics(id) {
    if (document.getElementById(id).classList.contains("hide_graphics")) {
        for (let i = 0; i < graphics.length; i++) {
            view.graphics.add(graphics[i])
        }
        document.getElementById(id).classList.remove("hide_graphics")
        document.getElementById(id).classList.add("show_graphics")

    } else {
        for (let i = 0; i < graphics.length; i++) {
            view.graphics.remove(graphics[i])
        }
        document.getElementById(id).classList.remove("show_graphics")
        document.getElementById(id).classList.add("hide_graphics")
    }
}

// close when someone clicks on the 'x' symbol inside the overlay
function closeNav() {
    document.getElementById('open').style.visibility = 'visible';
    document.getElementById('myNav').style.width = '0%';
}

var btn_captcha = document.getElementById('captcha');
btn_captcha.onclick = function () {
    console.log('captcha')
    location.assign('/captcha/');
}

var btn_overview = document.getElementById('overview');
btn_overview.onclick = function () {
    console.log('tiles_overview')
    location.assign('/tiles_overview/');
}

