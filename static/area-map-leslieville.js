// Create the Google Map
let a = 43.66614
let b = -79.33425
let myLatlng = new google.maps.LatLng(a, b);
let map = new google.maps.Map(document.getElementById('map'), {
	center : myLatlng,
	zoom   : 15
});

