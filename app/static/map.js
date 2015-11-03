

var scriptEl = document.createElement('script');
scriptEl.type = 'text/javascript';
scriptEl.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyACtYXfgytJqOg762NyUUxmjJbw7Fppl1I&sensor=true';
document.getElementsByTagName('head')[0].appendChild(scriptEl);

var scriptEl = document.createElement('script');
scriptEl.type = 'text/javascript';
scriptEl.src = 'gmaps.js';
document.getElementsByTagName('head')[0].appendChild(scriptEl);

/*
var map = new GMaps({
    el: '#map',
    lat: -12.043333,
    lng: -77.028333
});
*/
