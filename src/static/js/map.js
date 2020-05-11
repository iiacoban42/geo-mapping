 // import {transform} from 'ol/proj';
      // assuming that OpenLayers knows about EPSG:21781, see above

      var parser = new ol.format.WMTSCapabilities();
      var map;
      proj4.defs(
        "EPSG:28992",
        "+proj=sterea +lat_0=52.15616055555555 +lon_0=5.38763888888889 +k=0.9999079 +x_0=155000 +y_0=463000 +ellps=bessel +units=m +no_defs"
      );

      var myProjection = new ol.proj.Projection({
        code: "EPSG:28992",
        extent: [12628.0541, 308179.0423, 283594.4779, 611063.1429],
        units: "m",
      });
      ol.proj.addProjection(myProjection);
      //const swissCoord = transform([8.23, 46.86], 'EPSG:4326', 'EPSG:28992');
      loadMaps();
      async function loadMaps() {
        await fetchMap(1815);
        await fetchMap(1875);
        await fetchMap(1915);
        await fetchMap(1945);
        await fetchMap(1955);
        await fetchMap(1965);
        await fetchMap(1975);

        await fetchMap(1980);
        await fetchMap(1985);
        await fetchMap(1990);
        await fetchMap(1995);
        await fetchMap(2000);
        await fetchMap(2005);
        await fetchMap(2010);

        await fetchMap(2015);
        await fetchMap(2017);
        await fetchMap(2018);
        setTimeout(function () {
          map.addLayer(vectorLayer);
        }, 18000);
      }

      /*
    var countriesSource = new ol.source.GeoJSON({
          projection: 'EPSG:28992',
          url: '../data/data.json'
        });

        countriesSource.once('change', function(evt) {
          if (this.getState() == 'ready') {
            console.log(this.getFeatures()[0].getGeometry().getCoordinates());
            console.log(this.getFeatures()[0].getGeometry().clone().transform('EPSG:28992','EPSG:4326').getCoordinates());
          }
        });

    var vectorLayer = new ol.layer.Vector({
          title: "data",
        source: countriesSource

    });
    */

      /*
     var flightsSource = new ol.source.Vector({
            wrapX: false,
            attributions: 'Flight data by ' +
                  '<a href="http://openflights.org/data.html">OpenFlights</a>,',
            loader: function() {

              var url = '../data/data.json';
              fetch(url).then(function(response) {

                          return response.json();
                  }).then(function(json){


                       var geom = [];
                        json.forEachFeature( function(feature) { console.log("hi"); geom.push(new ol.Feature(feature.getGeometry().clone().transform('EPSG:4326', 'EPSG:28992'))); } );
                          var writer = new ol.format.GeoJSON();
                          var geoJsonStr = writer.writeFeatures(geom);
                          console.log(geoJsonStr);

                  });
            }
     });
     */
      var yourVectorSource = new ol.source.Vector({
        projection: "EPSG:28992",
        url: "../data/data.geojson",
        format: new ol.format.GeoJSON(),
      });
      /*
    yourVectorSource.once('change', function(evt) {
          if (this.getState() == 'ready') {
                //for (int i=0; i<this.getFeatures().size(); i++){
                     console.log(this.getFeatures()[8].getGeometry().getCoordinates());
                     var geometry = this.getFeatures()[8].getGeometry();
                     geometry.transform(ol.proj.get('EPSG:4326'), ol.proj.get('EPSG:28992'));
            console.log(geometry.getCoordinates());
               // }

          }
        });
    */
      var vectorLayer = new ol.layer.Vector({
        source: yourVectorSource,
        title: "data",
        opacity: 0.8,
        baseLayer: true,
      });
      vectorLayer.setZIndex(10000);

      var controller = new ol.control.LayerPopup();
      //setTimeout(function(){ controller.drawPanel() }, 10000);

      function fetchMap(year) {
        fetch(
          "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" +
            year +
            "/MapServer/WMTS/1.0.0/WMTSCapabilities.xml"
        )
          .then(function (response) {
            return response.text();
          })
          .then(function (text) {
            var result = parser.read(text);
            var options = ol.source.WMTS.optionsFromCapabilities(result, {
              layer: "Historische_tijdreis_" + year,
              matrixSet: "default028mm",
            });

            var tileLayer = new ol.layer.Tile({
              opacity: 1,
              title: year,
              baseLayer: true,
              source: new ol.source.WMTS(
                /** @type {!module:ol/source/WMTS~Options} */ (options)
              ),
            });
            tileLayer.setZIndex(parseInt(year));
            map.addLayer(tileLayer);
          });
      }

      // The map
      //var osm_layer = new ol.layer.OSM({title:"basis"});

      var osm = new ol.layer.Tile({
        title: "OSM",
        baseLayer: true,
        source: new ol.source.OSM(),
        visible: true,
        type: "base",
      });

      map = new ol.Map({
        layers: [],
        target: "map",
        controls: ol.control.defaults().extend([controller]),
        view: new ol.View({
          center: [155000, 463000],
          projection: myProjection,
          zoom: 0,
        }),
      });

      map.getLayerGroup().on("change", function () {
        console.log("change", arguments);
      });
