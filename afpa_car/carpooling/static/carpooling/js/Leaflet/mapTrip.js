var startLat = _.replace($('#start_lat').val(), ',', '.')
var startLng = _.replace($('#start_lng').val(), ',', '.')
var destinationLat = _.replace($('#destination_lat').val(), ',', '.')
var destinationLng = _.replace($('#destination_lng').val(), ',', '.')

// Variables pour création de la carte
var mbUrl = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoia2FrbGVtYWthayIsImEiOiJjamxjMXpiMmQxMHV3M3dwZzB0bnk1c2Q2In0.LjmVM42iRFL4tU3TIzrgHw';
var mbAttr = 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>';
var streets  = L.tileLayer(mbUrl, {id: 'mapbox.streets',   attribution: mbAttr}),
    satellite  = L.tileLayer(mbUrl, {id: 'mapbox.satellite',   attribution: mbAttr}),
    darkgrayscale   = L.tileLayer(mbUrl, {id: 'mapbox.dark', attribution: mbAttr});

// Création de la carte
var map = L.map('mapTrip', { layers: streets });

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

// Ajout du systeme de Routing (librairie leaflet-routing-machine)
L.Routing.control({
    waypoints: [
        L.latLng(startLat, startLng),
        L.latLng(destinationLat, destinationLng)
    ],
    router: myRouter,
    geocoder: MapGeocoderProvider,
    addWaypoints: false,
    draggableWaypoints: false,
    lineOptions: {
        styles: [
            {color: 'black', opacity: 0.5, weight: 11},
            {color: 'indigo', opacity: 0.9, weight: 9},
            {color: 'white', opacity: 1, weight: 3}
        ]
    },
    show: false,
})
.addTo(map);