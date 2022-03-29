// Create the Google Map
let a = 43.66614
let b = -79.33425
let myLatlng = new google.maps.LatLng(a, b);
let map = new google.maps.Map(document.getElementById('map'), {
	center : myLatlng,
	zoom   : 15
});

document.getElementById('lat').setAttribute('value', a);
document.getElementById('long').setAttribute('value', b);

// Place a draggable marker on the map
let marker = new google.maps.Marker({
	position  : myLatlng,
	map       : map,
	draggable : true,
	title     : 'Drag me!'
});

google.maps.event.addListener(
	marker,
	'dragend',
	function(evt) {
		let a = evt.latLng.lat().toFixed(5);
		let b = evt.latLng.lng().toFixed(5);
		let lat = parseFloat(a);
		let long = parseFloat(b);
		document.getElementById('lat').setAttribute('value', lat);
		document.getElementById('long').setAttribute('value', long);
	});

map.setCenter(marker.position);
marker.setMap(map);
