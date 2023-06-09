(function (window, document, $) {
    $(function () {
        'use strict';

        // $("#startDate").datepicker();
        // $("#endDate").datepicker();

        $("#startDate").datetimepicker();
        $("#endDate").datetimepicker();


        function hideAlert() {
            $('#alert').on('click', function () {
                $(this).hide();
            })
            $('#alert').delay(5000).fadeOut('fast');
        }

        var mymap = L.map('mapId', {
            center: [-33.3, -70.66],
            zoom: 6,
        });


        var osMaps = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        });
        mymap.addLayer(osMaps);

        function getradius(feature) {
            var radius = feature.properties.radius
            var radio = {
                radius: radius
            }
            return radio
        }

        function htmlPopUp(props) {
            let html = '<h4>Hotspot</h4>' +
                'Detection Time: ' + props.tz + '<br/>' +
                'Satellite: ' + props.satellite + '<br/>' +
                'Detection Uncertainty: ' + props.radius + ' meters' + '<br/>'
            return html
        };


        function renderHotspots(response, leafletMap) {
            // function renderHotspots(response, leafletMap, jsonLayer) {
            // function renderHotspots(response, leafletMap) {
            // jsonLayer
            //     // leafletMap.eachLayer(function (layer) {
            //     leafletMap.removeLayer(layer)
            // })
            // jsonLayer.clearLayers()
            // if (jsonLayer !== undefined) {

            // leafletMap.eachLayer(function (layer) {
            //     // leafletMap.removeLayer(layer)
            //     if (layer._leaflet_id === 2) { console.log(layer) }
            // })
            // jsonLayer.clearLayers()
            // leafletMap.removeLayer(jsonLayer);
            // }
            // jsonLayer.pointToLayer(feature, latlng) {
            //         return L.circle(latlng, getradius(feature))
            //         // return L.circleMarker(latlng, hotspotMarker)
            //     }.addTo(leafletMap)
            let jsonLayer = L.geoJSON(response, {
                // jsonLayer = L.geoJSON(response, {
                pointToLayer: function (feature, latlng) {
                    return L.circle(latlng, getradius(feature))
                    // return L.circleMarker(latlng, hotspotMarker)
                },
                filter: function (feature, layer) {
                    return feature.properties.radius
                }
            }).bindPopup(function (layer) {
                return htmlPopUp(layer.feature.properties)
            }).addTo(leafletMap)

            leafletMap.fitBounds(jsonLayer.getBounds())

            // leafletMap.removeLayer(jsonLayer);
        }


        var hotspotMarker = {
            radius: 8,
            fillColor: "#ff7800",
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8,
        }

        $.ajax({
            type: "get",
            url: "/hotspots/",
            // url: "http://localhost:8000/hotspots/",
            // url: "http://localhost:8000/hotspots/redis",
            // url: "http://localhost:8000/hotspots/postgis",
            data: {
                "start_date": '2023-02-19 00:00:00',
                "end_date": '2023-02-21 00:00:00',
                "bounding_box": '-36.52,-72.75,-36.70,-73.12'
            },
            dataType: "json",
            statusCode: {
                200: function (response) {
                    // sessionStorage.removeItem("access_token")
                    // $("#alert").show()
                    // $("#alert").text("rendered successfully")
                    // $("#alert").addClass("alert-success")
                    // hideAlert()
                    // setTimeout(() => {
                    //     window.location.href = 'dashboard';
                    // }, 3000);
                },
                // 401: function (response) {
                //     // sessionStorage.removeItem("access_token")
                //     $("#alert").show()
                //     $("#alert").text(response.responseJSON.detail + ", please login again")
                //     $("#alert").addClass("alert-warning")
                //     hideAlert()
                //     setTimeout(() => {
                //         window.location.href = 'users/logout';
                //     }, 5000);
                // },
                500: function (response) {
                    $('#download-loader').hide();
                    $('#dataDownloader').hide();
                    $("#alert").show()
                    // $("#alert").text(response.responseJSON.message)
                    $("#alert").text(response.statusText + ' ' + response.status)
                    $("#alert").addClass("alert-warning")
                    hideAlert()
                }
            },
            success: function (response) {


                renderHotspots(response, mymap)

            }
        });

        function prepareDate(date) {
            let splitDate = date.split("/")
            // let newDate = splitDate[2] + "-" + splitDate[0] + "-" + splitDate[1] + " 00:00:00"
            // let newDate = splitDate[2] + "-" + splitDate[1] + "-" + splitDate[0] + " 00:00:00"
            let newDate = splitDate[0] + "-" + splitDate[1] + "-" + splitDate[2] + ":00"
            // let newDate = splitDate[2] + "-" + splitDate[0] + "-" + splitDate[1]
            return newDate
        }

        function getBoundingBox(leafletBounds) {
            var ne_lat = leafletBounds._northEast.lat
            var ne_lng = leafletBounds._northEast.lng
            var sw_lat = leafletBounds._southWest.lat
            var sw_lng = leafletBounds._southWest.lng
            var bbox = ne_lat + "," + ne_lng + "," + sw_lat + "," + sw_lng
            return bbox

        }
        $("#dateRange").submit(function (e) {
            e.preventDefault();

            let startDate = prepareDate($("#startDate").val());
            let endDate = prepareDate($("#endDate").val());
            let bbox = getBoundingBox(mymap.getBounds())
            $.ajax({
                type: "get",
                url: "/hotspots/",
                // url: "http://localhost:8000/hotspots/",
                data: {
                    "start_date": startDate,
                    "end_date": endDate,
                    "bounding_box": bbox
                },
                dataType: "json",
                statusCode: {
                    200: function (response) {
                        // sessionStorage.removeItem("access_token")
                        // $("#alert").show()
                        // $("#alert").text("rendered successfully")
                        // $("#alert").addClass("alert-success")
                        // hideAlert()
                        // setTimeout(() => {
                        //     window.location.href = 'dashboard';
                        // }, 3000);
                    },
                    // 401: function (response) {
                    //     // sessionStorage.removeItem("access_token")
                    //     $("#alert").show()
                    //     $("#alert").text(response.responseJSON.detail + ", please login again")
                    //     $("#alert").addClass("alert-warning")
                    //     hideAlert()
                    //     setTimeout(() => {
                    //         window.location.href = 'users/logout';
                    //     }, 5000);
                    // },
                    500: function (response) {
                        $('#download-loader').hide();
                        $('#dataDownloader').hide();
                        $("#alert").show()
                        // $("#alert").text(response.responseJSON.message)
                        $("#alert").text(response.statusText + ' ' + response.status)
                        $("#alert").addClass("alert-warning")
                        hideAlert()
                    }
                },
                success: function (response) {
                    // let jsonLayer = L.geoJSON(response).addTo(mymap)
                    // renderHotspots(response, mymap, jsonLayer)
                    // let jsonLayer
                    // renderHotspots(response, mymap)
                    // renderHotspots(response, mymap, jsonLayer)
                    // try {
                    if (response.features.length === 0) {
                        alert("No hotspots detected in the map extent you are searching. Try again either with a different date range or map extent")
                    }
                    renderHotspots(response, mymap)
                    // } catch (error) {
                    // error.statusCode = 500    
                    // }
                }
            });



        });


    });
}(window, document, jQuery));