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

        // create a symbol for drawing the point
        var pointSymbol = {
            type: 'simple-marker',             // autocasts as new SimpleMarkerSymbol()
            color: [226, 119, 40],
            width: 8,
            outline: {
                color: [255, 255, 255],
                width: 4
            }
        };

        // template for points on map
        var template = {
            title: '{Label}',
            content: [
                {
                    type: 'fields',
                    fieldInfos: [
                        {
                            fieldName: 'Name'
                        },
                        {
                            fieldName: 'Other'
                        }
                    ]
                }
            ]
        };

        // get json with points
        // document.onreadystatechange = load_labels()
        // document.onreadystatechange ,

        layer.on(["layerview-create", "layerview-destroy"], async function () {
                let year = document.getElementById('current').innerHTML
                const req_building = {"year": year, "label": "building"}
                // console.log("bbbbbbbbbbbbbbbbbb")
                const json_building = await getAllLabels(req_building);
                const req_land = {"year": year, "label": "land"}
                const json_land = await getAllLabels(req_land);
                const req_water = {"year": year, "label": "water"}
                const json_water = await getAllLabels(req_water);

                // display points in view

                // console.log(json_building)
                // console.log(json_building.length)


                var symbol_building = {
                    type: "simple-fill",  // autocasts as new SimpleFillSymbol()
                    color: [130, 130, 130, 0.2],
                    style: "solid",
                    outline: {  // autocasts as new SimpleLineSymbol()
                        color: "black",
                        width: 10
                    }
                };

                var symbol_land = {
                    type: "simple-fill",  // autocasts as new SimpleFillSymbol()
                    color: [227, 197, 89, 0.2],
                    style: "solid",
                    outline: {  // autocasts as new SimpleLineSymbol()
                        color: "orange",
                        width: 5
                    }
                };

                var symbol_water = {
                    type: "simple-fill",  // autocasts as new SimpleFillSymbol()
                    color: [10,10, 204, 0.2],
                    style: "solid",
                    outline: {  // autocasts as new SimpleLineSymbol()
                        color: "blue",
                        width: 1
                    }
                };

                for (let i = 0; i < json_building.length; i++) {
                    var x_coord = json_building[i].x_coord;
                    var y_coord = json_building[i].y_coord;
                    var circleGeometry = new Circle([y_coord,x_coord], {
                        radius: 203,
                        radiusUnit: "meters",
                        spatialReference: {wkid: 28992},
                        geodesic: true
                    });
                    graphics[graphics.length] = new Graphic({geometry: circleGeometry.extent, symbol: symbol_building});
                }

                 for (let i = 0; i < json_land.length; i++) {
                    x_coord = json_land[i].x_coord;
                    y_coord = json_land[i].y_coord;
                    circleGeometry = new Circle([y_coord,x_coord], {
                        radius: 203,
                        radiusUnit: "meters",
                        spatialReference: {wkid: 28992},
                        geodesic: true
                    });
                    graphics[graphics.length] = new Graphic({geometry: circleGeometry.extent, symbol: symbol_land});
                }

                 for (let i = 0; i < json_water.length; i++) {
                    x_coord = json_water[i].x_coord;
                    y_coord = json_water[i].y_coord;
                    circleGeometry = new Circle([y_coord,x_coord], {
                        radius: 203,
                        radiusUnit: "meters",
                        spatialReference: {wkid: 28992},
                        geodesic: true
                    });
                    graphics[graphics.length] = new Graphic({geometry: circleGeometry.extent, symbol: symbol_water});
                }
            });
        // add div element to show coords
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


        view.on('click', function (event) {
            event.stopPropagation(); // overwrite default click-for-popup behavior
            // Get the coordinates of the click on the view
            year = document.getElementById('current').innerHTML
            coord_x_db = Math.round((event.mapPoint.x + 30527385.66843) / 406.55828)
            coord_y_db = Math.round((event.mapPoint.y - 31113121.21698) / (-406.41038))
            const req = {'year': year, 'x_coord': coord_x_db, 'y_coord': coord_y_db}

            const json = getLabels(req);
            console.log(json)


            // template for labelled tiles on map
            // if(json.building === true || json.land === true || json.water === true) {
            view.popup.open({
                title: 'Tile from year ' + year + ' with coords x= ' + coord_x_db + ', y= ' + coord_y_db + '!!!',
                content: [
                    {
                        type: 'fields',
                        fieldInfos: [
                            {
                                building: json.building
                            },
                            {
                                land: json.land

                            },
                            {
                                water: json.water
                            },
                        ]
                    }
                ],
                location: event.mapPoint // Set the location of the popup to the clicked location
            });
            view.popup.content = view.spatialReference.wkid.toString();
            // }
        });
        var searchWidget = new Search({view: view});
        view.ui.add(searchWidget, 'top-right');


        // change years based on the selection from the menu
        $(document).ready(function () {
                $(menu).click(function (event) {
                    if (event.target.id !== 'menu') {
                        var year = event.target.id
                        // console.log(year)
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


async function getLabels(req) {
    const response = await fetch('/get_labels/' + JSON.stringify(req));
    var data = await response.json()
    view.popup.content += ('<br>Building: ' + Boolean(data.building))
    view.popup.content += ('<br>Land: ' + Boolean(data.land))
    view.popup.content += ('<br>Water: ' + Boolean(data.water))
}

async function getAllLabels(req) {
    const response = await fetch('/get_all_labels/' + JSON.stringify(req));
    var data = await response.json()
    return data
}

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

