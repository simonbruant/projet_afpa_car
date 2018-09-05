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

// Création d'un champ de recherche d'adresse
var MapGeocoder = L.Control.geocoder({
    collapsed: false,
    placeholder: 'Recherche...',
    errorMessage: 'Désolé nous ne trouvons pas cette adresse...',
    geocoder: MapGeocoderProvider
});

// Définition et Traduction du router
var myRouter = L.Routing.mapbox('pk.eyJ1Ijoia2FrbGVtYWthayIsImEiOiJjamxjMXpiMmQxMHV3M3dwZzB0bnk1c2Q2In0.LjmVM42iRFL4tU3TIzrgHw')
myRouter.options.language = 'fr';

// Ajout du systeme de Routing (librairie leaflet-routing-machine)
L.Routing.control({
    waypoints: [
        L.latLng(43.690160349425206, 3.881751894950867),
        L.latLng(43.56499, 3.8453)
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
/*.on('routeselected', function(e) {
    var route = e.route
    var time = route.summary.totalTime
    var heure = Math.floor(time/3600);
    time = time - heure*3600
    var min = Math.floor(time/60);
    var sec = Math.floor(time - min * 60);
    console.log(route.inputWaypoints[0]);
    for (var i = 0 ; i < route.instructions.length-1 ; i++) {
        console.log(route.instructions[i].text)
    }
    console.log("Depart : Latitude : " + route.inputWaypoints[0].latLng.lat + " Longitude : " + route.inputWaypoints[0].latLng.lng)
    console.log("Arrivée : Latitude : " + route.inputWaypoints[1].latLng.lat + " Longitude : " + route.inputWaypoints[1].latLng.lng)
    console.log("Distance : " + route.summary.totalDistance/1000 + "km")
    console.log("Durée : " + heure + "h" + min + "m" + sec + "s")
})*/
.addTo(map);

/* Fonction pour ajouter un marker au clic de la map avec un Popup contenant les coordonnées du point et un bouton supprimer */
/*map.on('click', onMapClick);
var markers = []
function onMapClick(e) {
    var id
    if (markers.length < 1) id = 0
    else id = markers[markers.length - 1]._id + 1
    var popupContent =
        'Vous avez cliqué aux coordonnées : ' + 
        e.latlng.lat.toString() + ', ' + 
        e.latlng.lng.toString() + '<br>' +
        '<button onclick="clearMarker(' + id + ')">Supprimer ce point</button>';
    myMarker = L.marker([], { draggable: false }).setLatLng(e.latlng);
    myMarker._id = id
    var myPopup = myMarker.bindPopup(popupContent, { closeButton: false });
    map.addLayer(myMarker)
    markers.push(myMarker)
    };

function clearMarker(id) {
    var new_markers = []
    markers.forEach(function(marker) {
        if (marker._id == id) map.removeLayer(marker)
        else new_markers.push(marker)
    })
    markers = new_markers
};*/
