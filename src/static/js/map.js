var map;
var view;

require(["esri/Map", "esri/views/MapView", "esri/layers/TileLayer", "esri/Graphic", 'esri/geometry/Extent',
'esri/widgets/Search', "esri/geometry/Circle", "dojo/domReady!"],
    function (Map, MapView, TileLayer, Graphic, Extent, Search, Circle) {

        // initial map
        var baseLayer = new TileLayer({
            url: 'https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_2016/MapServer'
        });
        map = new Map('map', {
            center: [-122.45, 37.75],
        });

        map.add(baseLayer)

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
        document.onreadystatechange = async function () {
            const response = await fetch('/get_markers');
            const json = await response.json();

            var labels = json.labels
            var points = json.points
            // display points in view
            for (let i = 0; i < points.length; i++) {
                var pointGraphic = new Graphic({geometry: points[i], symbol: pointSymbol, attributes: labels[i]});
                pointGraphic.popupTemplate = template
                view.graphics.add(pointGraphic);

                var lat = parseFloat(points[i].latitude), long = parseFloat(points[i].longitude)

                var circleGeometry = new Circle([long, lat],{
                    radius: 203,
                    radiusUnit: "meters",
                    spatialReference: { wkid: 28992 } ,
                    geodesic: true 
                  });
                

                var symbol = {
                type: "simple-fill",  // autocasts as new SimpleFillSymbol()
                    color: [ 51,51, 204, 0.2 ],
                    style: "solid",
                    outline: {  // autocasts as new SimpleLineSymbol()
                      color: "white",
                      width: 1
            }
                  };
                
                view.graphics.add(new Graphic({geometry:circleGeometry.extent, symbol:symbol}));
        }
        }

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
                        console.log(year)
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

// open when someone clicks on the span element
function openNav() {
    document.getElementById('open').style.visibility = 'hidden';
    document.getElementById('myNav').style.width = '7%';

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

