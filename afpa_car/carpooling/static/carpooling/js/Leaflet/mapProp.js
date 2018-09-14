var startLat = _.replace($('#start_lat').val(), ',', '.')
var startLng = _.replace($('#start_lng').val(), ',', '.')
var destinationLat = _.replace($('#destination_lat').val(), ',', '.')
var destinationLng = _.replace($('#destination_lng').val(), ',', '.')
var userStartLat = _.replace($('#user_start_lat').val(), ',', '.')
var userStartLng = _.replace($('#user_start_lng').val(), ',', '.')
var userDestinationLat = _.replace($('#user_destination_lat').val(), ',', '.')
var userDestinationLng = _.replace($('#user_destination_lng').val(), ',', '.')
var trip_user = $('#trip_user').val()

// Variables pour création de la carte
var mbUrl = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoia2FrbGVtYWthayIsImEiOiJjamxjMXpiMmQxMHV3M3dwZzB0bnk1c2Q2In0.LjmVM42iRFL4tU3TIzrgHw';
var mbAttr = 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>';
var streets  = L.tileLayer(mbUrl, {id: 'mapbox.streets',   attribution: mbAttr}),
    satellite  = L.tileLayer(mbUrl, {id: 'mapbox.satellite',   attribution: mbAttr}),
    darkgrayscale   = L.tileLayer(mbUrl, {id: 'mapbox.dark', attribution: mbAttr});

// Création de la carte
var map = L.map('mapProp', { layers: streets })

// Définition des diférents layers
var baseLayers = {
    "Streets": streets,
    "Satellite": satellite,
    "Dark": darkgrayscale,
};

// Ajout du controle des layers
L.control.layers(baseLayers).addTo(map);

// Définition du geocoder (librairie leaflet-control-geocoder) - Systeme de conversion adresse Postale <-> GPS
var MapGeocoderProvider = new L.Control.Geocoder.Nominatim()

// Définition et Traduction du router
var myRouter = L.Routing.mapbox('pk.eyJ1Ijoia2FrbGVtYWthayIsImEiOiJjamxjMXpiMmQxMHV3M3dwZzB0bnk1c2Q2In0.LjmVM42iRFL4tU3TIzrgHw')
myRouter.options.language = 'fr';

// Trajet recherché
var searched_trip = L.Routing.control({
    waypoints: [
        L.latLng(startLat, startLng),
        L.latLng(destinationLat, destinationLng)
    ],
    router: myRouter,
    geocoder: MapGeocoderProvider,
    position: 'bottomright',
    draggableWaypoints: false,
    addWaypoints: false,
    lineOptions: {
        styles: [
            {color: 'black', opacity: 0.5, weight: 11},
            {color: 'indigo', opacity: 0.9, weight: 9},
            {color: 'white', opacity: 1, weight: 3}
        ]
    },
    showAlternatives: false,
    fitSelectedRoutes: false,
    altLineOptions: {
        styles: [
            {color: 'black', opacity: 0.5, weight: 11},
            {color: 'grey', opacity: 0.9, weight: 9},
            {color: 'white', opacity: 1, weight: 3}
        ]
    },
})
.addTo(map);

// Trajet de l'utilisateur
var user_trip = L.Routing.control({
    waypoints: [
        L.latLng(userStartLat, userStartLng),
        L.latLng(userDestinationLat, userDestinationLng)
    ],
    router: myRouter,
    geocoder: MapGeocoderProvider,
    position: 'bottomright',
    draggableWaypoints: false,
    addWaypoints: false,
    fitSelectedRoutes: 'smart',
    lineOptions: {
        styles: [
            {color: 'black', opacity: 0.5, weight: 11},
            {color: 'green', opacity: 0.9, weight: 9},
            {color: 'white', opacity: 1, weight: 3}
        ]
    }
})
.on('waypointschanged', function(e) {
    for (var j = 1; j < e.waypoints.length-1; j++) {
        console.log("latitude : " + e.waypoints[j].latLng.lat + ", Longitude : " + e.waypoints[j].latLng.lng)
        console.log(trip_user)
    }
    if (e.waypoints.length == 3) {
        user_trip.options.addWaypoints = false
    }
}).addTo(map);

searched_trip.hide();
user_trip.hide();

// new Vue ({
//     el: '#map',
//     created() {
//         if (trip_user) {
//             console.log("user", user_trip.options.addWaypoints)
//             console.log("search", searched_trip.options.addWaypoints)
//             // user_trip.options.addWaypoints = true
//         } else {
//             console.log("user", user_trip.options.addWaypoints)
//             console.log("search", searched_trip.options.addWaypoints)
//         // searched_trip.options.addWaypoints = true
//     }
// }
// })