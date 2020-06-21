
var map;
var view;
var featureLayer;
var objectLayer;

graphics = new Map()

require(["esri/Map", "esri/views/MapView", "esri/widgets/Legend/LegendViewModel", "esri/widgets/LayerList", "esri/widgets/Legend",
        "esri/layers/TileLayer", "esri/layers/GraphicsLayer", "esri/layers/FeatureLayer", "esri/renderers/UniqueValueRenderer",
        "esri/Graphic", 'esri/geometry/Extent', "esri/geometry/Polygon", "esri/geometry/Circle", "esri/symbols/SimpleFillSymbol",
        "esri/widgets/Editor", "esri/views/layers/FeatureLayerView", "esri/widgets/Editor/EditorViewModel", "dojo/domReady!"],
    function (Map, MapView, LegendViewModel, LayerList, Legend, TileLayer, GraphicsLayer, FeatureLayer, UniqueValueRenderer, Graphic, Extent, Polygon, Circle, SimpleFillSymbol, Editor) {

        // initial map
        var layer = new TileLayer({
            url: 'https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_2016/MapServer'
        });
        map = new Map('map', {
            center: [-122.45, 37.75],
        });

        map.add(layer)

        // Create the feature layer, used for the overlay
        setupFeatureLayer(FeatureLayer);
        map.add(featureLayer)
        setupObjectLayer(FeatureLayer);
        map.add(objectLayer)

        // map is added to the view
        view = new MapView({
            container: 'map',
            map: map,
        });

        const editor = new Editor({
            layerInfos: [{
                enabled: true, // default is true, set to false to disable editing functionality
                addEnabled: true, // default is true, set to false to disable the ability to add a new feature
                updateEnabled: true, // default is true, set to false to disable the ability to edit an existing feature
                deleteEnabled: true, // default is true, set to false to disable the ability to delete features
                featureLayer: featureLayer
            }],
            view: view,
        });
        view.ui.add(editor, 'top-right')


        $(predictions).click(async function load_labels(event) {
            let label = event.target.id
            // if user changes year, exit function
            let abortController = new AbortController();
            document.getElementById(label).innerHTML = "loading..."
            let year = document.getElementById('current').innerHTML
            $(menu).click(function () {
                document.getElementById(label).innerHTML = label
                abortController.abort()
            });
            const req = {"year": year, "label": label}
            const response = await fetch('/get_all_labels/' + JSON.stringify(req), {signal: abortController.signal});
            try {
                var json = await response.json()

                console.log("Fetched " + json.length + " tiles")
                // display points in view

                circleProperties = {
                    radius: 203,
                    radiusUnit: "meters",
                    spatialReference: {wkid: 28992},
                    geodesic: true
                }

                edits = {
                    addFeatures: [],
                    updateFeatures: []
                }

                objectEdits = {
                    addFeatures: [],
                    updateFeatures: []
                }

                for (let i = 0; i < json.length; i++) {
                    mapKey = json[i].x_coord + " " + json[i].y_coord;

                    var newEntry = true;
                    // If the tile graphic already exists (for another label) get it from the Map
                    if (graphics.has(mapKey)) {
                        graphic = graphics.get(mapKey)
                        console.log(mapKey + "->" + label)
                        newEntry = false;
                    } else { // If this tile doesn't have any labels yet
                        var attr = {
                            Longitude: json[i].x_coord,
                            Latitude: json[i].y_coord,
                            Building: "false",
                            Land: "false",
                            Water: "false",
                        }

                        var circleGeometry = new Circle([json[i].x_coord, json[i].y_coord], circleProperties);
                        graphic = new Graphic({
                            geometry: Polygon.fromExtent(circleGeometry.extent),
                            attributes: attr
                        });
                    }
                    if (label == "building")
                        graphic.setAttribute('Building', "true")

                    if (label == "land")
                        graphic.setAttribute('Land', "true")

                    if (label == "water")
                        graphic.setAttribute('Water', "true")

                    if (label == "church") {
                        graphic = new Graphic({
                          geometry: circleGeometry.extent,
                        });
                        objectEdits.addFeatures.push(graphic)
                    }

                    if(label != "church"){
                        graphics.set(mapKey, graphic)
                        if (newEntry) {
                            edits.addFeatures.push(graphic)
                        } else {
                            edits.updateFeatures.push(graphic)
                        }
                    }
                }

                console.log("Total tiles: " + graphics.size)
                featureLayer.applyEdits(edits)
                objectLayer.applyEdits(objectEdits)
            } catch (exception) {
                console.error(exception);
                console.error(exception.lineNumber);
                alert("Not yet classified, do some CAPTCHA")
            }
            document.getElementById(label).innerHTML = label
        });
//         layerWidget = new LayerList({
//             map: map,
//             subLayers: false,
//             layers: [
//                 // {layer: ortho2013Layer,
//                 // visibility: false
//                 // },
//                 {
//                     layer: "Building",
//                     subLayers: false,
//                     visbility: true,
//                     id: "Milepost Labels"
//                 },
//                 {
//                     layer: "Land",
//                     visibility: false
//                 },
//                 {
//                     layer: "Water",
//                     visibility: false
//                 },
//                 {
//                     layer: "streamLayer",
//                     visibility: false
//                 },
//
//             ]
//         }, "layerList");
//
//         var layerList = new LayerList({
//             map: map,
//             showLegend: false,
//             showSubLayers: false,
//             showOpacitySlider: true,
//             layer: featureLayer
//         })
//         // view.ui.add(legend, 'bottom-right')
//         var legend = new Legend({
//             view: view,
//             content: [{
//                 layer: featureLayer,
//                 title: "Legend"
//             }],
//
//
//         });// Add a legend instance to the panel of a


        const legend = new Legend({
            // view: view,
            showLegend: true,
            showSubLayers: true,
            showOpacitySlider: true,
            viewModel: new LegendViewModel({
                view: view,
            }), content: [{
                layer: featureLayer,
                title: "Legend",

            }],
        });

        // ListItem in a LayerList instance
        const layerList = new LayerList({
            view: view,
            listItemCreatedFunction: function (event) {
                const item = event.item;
                // console.log(item.layer.layerId)
                //console.log(item.layer.operationalLayerType)
                //console.log(item.__accessorMetadata__)
                //console.log(item.layer.innerHTML)
                //console.log(item.layer.outFields)
                if (item.layer.geometryType === "polygon") {
                    // don't show legend twice
                    item.panel = legend,
                        open = 'false',
                        caption = "Labels",
                        item.title = "Classification Legend",

                        // Text with building does not disappear??
                        item.caption = "Labels"
                }
            }
        });
        view.ui.add(layerList, "bottom-right");
        var coordsWidget = document.createElement('div');
        coordsWidget.id = 'coordsWidget';
        coordsWidget.className = 'esri-widget esri-component';
        coordsWidget.style.padding = '7px 15px 5px';
        view.ui.add(coordsWidget, 'bottom-left');

        // update lat, lon, zoom and scale
        // lat and lon are in other coord system for now (hopefully)
        function showCoordinates(event) {
            var coords = 'Latititude: ' + event.y + ' | Longitude: ' + event.x +
                ' | Scale 1:' + Math.round(view.scale * 1) / 1 +
                ' | Zoom ' + view.zoom +
                ' | EPSG:28992';
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
                        setupFeatureLayer(FeatureLayer);
                        setupObjectLayer(FeatureLayer);
                        map.add(featureLayer);
                        map.add(objectLayer);
                        document.getElementById('current').innerHTML = event.target.id;
                        closeNav();
                    }
                });
            }
        );
    }
);

function setupObjectLayer(FeatureLayer) {
            // Create the feature layer for objects
        var objectRenderer = {
            type: "simple",
            label: "Church",
            symbol: {
                type: "picture-marker",
                url: "/static/img/church.png",
                height: 18,
                width: 18
            }
          }

        objectLayer = new FeatureLayer({
            source: [],
            geometryType: "polygon",
            renderer: objectRenderer,
            objectIdField: "objectid",
            fields: [
                {
                    name: "objectid",
                    type: "oid"
                }
            ]
        });
}

function setupFeatureLayer(FeatureLayer) {
    // template for points on map
    var template = {
        title: "Tile | EPSG:4326",
        content: "<div>{Longitude}:{Latitude}<br>\
                        Building: {Building}<br>\
                        Land: {Land}<br>\
                        Water: {Water}</div>"
    };

    var renderer = {
        type: "unique-value",  // autocasts as new UniqueValueRenderer()
        field: "Building",
        field2: "Land",
        field3: "Water",
        fieldDelimiter: ":",
        defaultSymbol: {type: "simple-fill"},  // autocasts as new SimpleFillSymbol()
        uniqueValueInfos: [{
            value: "true:false:false",
            label: "Building",
            symbol: {
                type: "simple-fill",  // autocasts as new SimpleFillSymbol()
                color: [79, 71, 72, 0.7],
                style: "solid",
                outline: {
                    style: "none"
                }
            }
        }, {
            value: "false:true:false",
            label: "Land",
            symbol: {
                type: "simple-fill",
                color: [130, 189, 121, 0.9],
                style: "solid",
                outline: {
                    style: "none"
                }
            }
        }, {
            value: "false:false:true",
            label: "Water",
            symbol: {
                type: "simple-fill",
                color: [113, 199, 245, 0.8],
                style: "solid",
                outline: {
                    style: "none"
                }
            }
        },
            {
                value: "true:true:false",
                label: "Building & Land",
                symbol: {
                    type: "simple-fill",
                    color: [199, 182, 125, 0.7],
                    style: "solid",
                    outline: {
                        style: "none"
                    }
                }
            }, {
                value: "true:false:true",
                label: "Building & Water",
                symbol: {
                    type: "simple-fill",
                    color: [67, 102, 125, 0.6],
                    style: "solid",
                    outline: {
                        style: "none"
                    }
                }
            }, {
                value: "false:true:true",
                label: "Land & Water",
                symbol: {
                    type: "simple-fill",
                    color: [113, 163, 168, 0.7],
                    style: "solid",
                    outline: {
                        style: "none"
                    }
                }
            }, {
                value: "true:true:true",
                label: "Building & Land & Water",
                symbol: {
                    type: "simple-fill",
                    color: [150, 90, 78, 0.7],
                    style: "solid",
                    outline: {
                        style: "none"
                    }
                },
                outFields: ["label"],
            }],
        outFields: ["*"],

    }
// opacity with minDataVal and maxDataVal defined
    for (let x = 0; x < 8; x++)
        console.log(renderer[x])
    // real-world size for 2D tree canopies
    var colorVisVar = {
        // The type must be set to size
        type: "color",
        // Assign the field name to visualize with size
        field: "label",
        colors: [79, 71, 72, 0.7]
    };
    //renderer.visualVariables = [colorVisVar];
    featureLayer = new FeatureLayer({
        objectIdField: "objectid",
        fields: [
            {
                name: "objectid",
                type: "oid"
            },
            {
                name: "Longitude",
                type: "double"
            },
            {
                name: "Latitude",
                type: "double"
            },
            {
                name: "Building",
                type: "string"
            },
            {
                name: "Land",
                type: "string"
            },
            {
                name: "Water",
                type: "string"
            }
        ],
        source: [],
        popupTemplate: template,
        renderer: renderer,
        geometryType: "polygon",
        spatialReference: {wkid: 28992},
        outFields: ["objectid"],
        labelsVisible: 'true',
    });

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

window.addEventListener("load", function() {
    var btn_captcha = document.getElementById('go_captcha');
    btn_captcha.onclick = function () {
        console.log('captcha')
        location.assign('/captcha/');
    }

    var btn_overview = document.getElementById('overview');
    btn_overview.onclick = function () {
        console.log('tiles_overview')
        location.assign('/tiles_overview/');
    }

    var btn_train = document.getElementById('train');
    btn_train.onclick = function () {
        console.log('train')
        location.assign('/train/');
    }

    var captcha_form = document.getElementById('captcha_form');
    captcha_form.addEventListener('submit', function(){
        var uuid_input = document.getElementById('uuid_input');

        if(uuid_input.value != "")
            document.getElementById('captcha_block').style.display = "none";

        event.preventDefault();
    });

}, false);
//
// if (labels.includes(label)) {
//                view.whenLayerView(featureLayer).then(function (layerView) {
//                    layerView.queryFeatures({
//                        outFields: layerView.availableFields
//                    })
//                        .then(function (results) {
//                            console.log(results.features.length, " features returned");
//                        })
//                        .catch(function (error) {
//                            console.log("query failed: ", error);
//                        });
//                })
//            }

// view.ui.add(legend, "bottom-right");
// editor.viewModel.on(['awaiting-feature-creation-info', 'awaiting-feature-to-update'], function (event) {
//     console.log("SearchViewModel says: 'Search started'.");
// });
// edit.on("click", function () {
//     console.log("AAA")
// });
