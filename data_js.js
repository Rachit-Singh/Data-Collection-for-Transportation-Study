
// conversion of degree to radians
function deg2rad(deg) {
    return deg * (Math.PI/180);
}


// for calculation of distances between the lat-longs
function getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2) {
    var R = 6371; // Radius of the earth in km
    var dLat = deg2rad(lat2-lat1);  // deg2rad below
    var dLon = deg2rad(lon2-lon1); 
    var a = 
      Math.sin(dLat/2) * Math.sin(dLat/2) +
      Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * 
      Math.sin(dLon/2) * Math.sin(dLon/2)
      ; 
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
    var d = R * c; // Distance in km
    return d;
}


// to generate random lat longs in a circular region around a center
function randomGeo(center, radius) {
    var y0 = center.latitude;
    var x0 = center.longitude;
    var rd = radius / 111300;

    var u = Math.random();
    var v = Math.random();

    var w = rd * Math.sqrt(u);
    var t = 2 * Math.PI * v;
    var x = w * Math.cos(t);
    var y = w * Math.sin(t);

    return {
        'latitude': y + y0,
        'longitude': x + x0
    };
}


var stations_lat_longs = [[26.877242405049177, 80.97476738960607], [26.876515092089775, 80.9779860405909], [26.876591651569004, 80.9851958187969],
[26.870926110073405, 80.96905964852631], [26.866983031909268, 80.96120614012334], [26.870505011195853, 80.98871487720699], 
[26.870811265080512, 80.96142071685567], [26.878161109467353, 80.96674221981725], [26.881950686269487, 80.97927350098483], 
[26.873222985436726, 80.99815625342913]]; // stores lat-longs of the stations

var center = {"latitude": 26.871423770361474, "longitude": 80.97661274950404};  // center 
var myLocation = randomGeo(center, 20000);
var workPlaceLocation = randomGeo(center, 20000);


// for writing distances and lat-longs on the page
function printingJob() {
    var percentages = [20, 25, 30, 35, 40, 45, 50, 55, 60, 70];
    // selecting a random battery percentage everytime
    var battery = percentages[Math.round(Math.random()*percentages.length)];
    var x = document.getElementsByClassName("battery");
    for (let i=0; i<x.length; i++) { x[i].innerHTML = battery; }  // writing battery everywhere

    // writing time taken to charge 
    document.getElementById("fast_time").innerHTML = Math.round((100 - battery) * 20 / 80) ;
    document.getElementById("slow_time").innerHTML = Math.round((100 - battery) * 120 / 80) ;

    document.getElementById("position").innerHTML = "(" + myLocation.latitude.toFixed(5) + "," + myLocation.longitude.toFixed(5) + ")";  // writing the random location chosen
    document.getElementById("fast_cost").innerHTML = 5 * (100 - battery);  // writing cost of the recharge
    document.getElementById("slow_cost").innerHTML = 2 * (100 - battery);

    for (let i=0; i<stations_lat_longs.length; i++) {
        let dist1 = getDistanceFromLatLonInKm(stations_lat_longs[i][0], stations_lat_longs[i][1], myLocation.latitude, myLocation.longitude);  // finding distance
        let dist2 = getDistanceFromLatLonInKm(stations_lat_longs[i][0], stations_lat_longs[i][1], workPlaceLocation.latitude, workPlaceLocation.longitude);
        document.getElementById(String(i)+"ds").innerHTML = dist1.toFixed(2); // writing distance in the table
        document.getElementById(String(i)+"sw").innerHTML = dist2.toFixed(2);
    }
}