// Create the Google Map
let a = 43.66614
let b = -79.33425
let myLatlng = new google.maps.LatLng(a, b);
let map = new google.maps.Map(document.getElementById('map'), {
	center : myLatlng,
	zoom   : 15
});

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
		//document.getElementById('current').innerHTML = 
		//` ${evt.latLng.lat().toFixed(5)} , ${evt.latLng.lng().toFixed(5)}`;
		let a = evt.latLng.lat().toFixed(5);
		let b = evt.latLng.lng().toFixed(5);
		//window.alert(a);
		//window.alert(b);
		let lat = parseFloat(a);
		let long = parseFloat(b);
	
		document.getElementById('lat').setAttribute('value', lat);
		document.getElementById('long').setAttribute('value', long);
	
		//window.alert(lat);
		//window.alert(typeof long);
	}

	
);

google.maps.event.addListener(marker, 'dragstart', function(evt) {
	document.getElementById('current').innerHTML = '<p>Currently dragging marker...</p>';
});

map.setCenter(marker.position);
marker.setMap(map);
