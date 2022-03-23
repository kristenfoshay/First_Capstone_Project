// Create the Google Map
let some_data = $('#map-data').data();
let c = Object.values(some_data);
let a = c[0];
let b = c[1];

let myLatlng = new google.maps.LatLng(a, b);
let map = new google.maps.Map(document.getElementById('map'), {
	center : myLatlng,
	zoom   : 18
});

// Place a draggable marker on the map
let marker = new google.maps.Marker({
	position  : myLatlng,
	map       : map,
	draggable : false
});

map.setCenter(marker.position);
marker.setMap(map);
