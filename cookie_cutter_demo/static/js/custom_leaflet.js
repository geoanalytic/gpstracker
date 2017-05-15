/* Project specific Javascript goes here. */

/*
Formatting hack to get around crispy-forms unfortunate hardcoding
in helpers.FormHelper:

    if template_pack == 'bootstrap4':
        grid_colum_matcher = re.compile('\w*col-(xs|sm|md|lg|xl)-\d+\w*')
        using_grid_layout = (grid_colum_matcher.match(self.label_class) or
                             grid_colum_matcher.match(self.field_class))
        if using_grid_layout:
            items['using_grid_layout'] = True

Issues with the above approach:

1. Fragile: Assumes Bootstrap 4's API doesn't change (it does)
2. Unforgiving: Doesn't allow for any variation in template design
3. Really Unforgiving: No way to override this behavior
4. Undocumented: No mention in the documentation, or it's too hard for me to find
*/
$('.form-group').removeClass('row');
 
window.addEventListener("map:init", function (event) {
	
    var map = event.detail.map;

	// ----------------------------------------------------
	// Add Credits: 
	// ----------------------------------------------------
	map.attributionControl.addAttribution('Overlay data by  <a href="http://opendataareas.ca/" target="_blank">Open Data Areas Alberta</a>');
	map.attributionControl.addAttribution('Customization by <a href="http://www.geoanalytic.com" target="_blank">GeoAnalytic Inc</a>');

	var flyto = [
		{
		"name": "Alberta",
		"longitude": -115,
		"latitude": 54.5,
		"altitude": 1500000,
		"leaflet_zoom": 6,
		"heading": 0.0,
		"pitch": -90,
		"roll": 0
		},    {
		"name": "Beaver Hills",
		"longitude": -112.8803,
		"latitude": 53.4958,
		"altitude": 80000,
		"leaflet_zoom": 10,
		"heading": 0.0,
		"pitch": -90,
		"roll": 0
		},
		{
		"name": "Fort McMurray",
		"longitude": -111.0,
		"latitude": 56.2505,
		"altitude": 1000,
		"leaflet_zoom": 10,
		"heading": 0.0,
		"pitch": -35,
		"roll": 0
		},
		{
		"name": "Fox Creek",
		"longitude": -117.5261,
		"latitude": 54.0193,
		"altitude": 80000,
		"leaflet_zoom": 10,
		"heading": 0.0,
		"pitch": -90,
		"roll": 0
		},
		{
		"name": "RMH Sylvan",
		"longitude": -114.5047,
		"latitude": 52.4498,
		"altitude": 80000,
		"leaflet_zoom": 10,
		"heading": 0.0,
		"pitch": -90,
		"roll": 0
		},
		{
		"name": "Taber",
		"longitude": -112.0158,
		"latitude": 50.7021,
		"altitude": 80000,
		"leaflet_zoom": 10,
		"heading": 0.0,
		"pitch": -90,
		"roll": 0
		},
		{
		"name": "Utikuma Lake",
		"longitude": -115.3324,
		"latitude": 55.9393,
		"altitude": 80000,
		"leaflet_zoom": 10,
		"heading": 0.0,
		"pitch": -90,
		"roll": 0
		}
	];

	//----------------------------------------------------
	// Other Imagery, data
	//----------------------------------------------------
	var wmsLayer = L.tileLayer.betterWms('https://webmap.positionbot.com//mapserv/?map=/data/mapfiles/didsplus/didsplus.map&', {
		layers: 'DIDsPlus',
		format: 'image/png',
		transparent: true,
		attribution: "AltaLis"
    });  //.addTo(map);
//	wmsLayer.setZIndex(399);
	map.layerscontrol.addOverlay(wmsLayer, "DIDs+");
	
/*  //  (Added in common.py)	
    var wmsNTS = L.tileLayer('https://webmap.positionbot.com/mapcache/tms/1.0.0/NTS@g21/{z}/{x}/{y}.png', {
        tms: true,
		maxZoom: 21,
		attribution: "GeoAnalytic"
    });	
	map.layerscontrol.addOverlay(wmsNTS, "NTS Index");
*/	
/*  //  (Added in common.py)	
    var wmsDLS = L.tileLayer.betterWms('https://webmap.positionbot.com/mapserv/?map=/data/mapfiles/DLS/DLS.map&', {
		layers: 'default',
		format: 'image/png',
		transparent: true,
		attribution: "AltaLis"
    });  //.addTo(map);
//	wmsLayer.setZIndex(399);
	map.layerscontrol.addOverlay(wmsDLS, "Township System");
*/
/*
	var wmsLayer = L.tileLayer.betterWms('https://webmap.positionbot.com//mapserv/?map=/data/mapfiles/basemap/AltaLIS_20k.map&', {
		layers: 'default',
		format: 'image/png',
		transparent: true,
		attribution: "AltaLis"
    });  //.addTo(map);
//	wmsLayer.setZIndex(399);
	map.layerscontrol.addOverlay(wmsLayer, "Basemap Temp");
*/	
	//----------------------------------------------------
	// FlyTo Dropdown:
	//----------------------------------------------------		
	var flyToSelection = function(i){
		map.flyTo( [flyto[i].latitude, flyto[i].longitude], flyto[i].leaflet_zoom , {
			animate: true,
			duration: 6 // in seconds
		});
	};
	var flytoDropdownControl = L.control({position: 'topleft'});
	flytoDropdownControl.onAdd = function (map) {
		var flytoDropdown = L.DomUtil.create('select');
		flytoDropdown.onchange = function() {flyToSelection(this.selectedIndex)};
		for (var i = 0; i < flyto.length; i++){
			var flytoDropdownOption = document.createElement('option');
			flytoDropdownOption.text = flyto[i].name;
			flytoDropdown.appendChild(flytoDropdownOption);  		
		};
		flytoDropdown.firstChild.onmousedown = flytoDropdown.firstChild.ondblclick = L.DomEvent.stopPropagation;
		return flytoDropdown;
	};
	flytoDropdownControl.addTo(map);	
		
	
	
//	var topPane = map._createPane('leaflet-top-pane', map.getPanes().mapPane);
//	topPane.appendChild(wmsLayer.getContainer());
	//----------------------------------------------------
	// Mouse Position Plugin:
	//----------------------------------------------------	
    L.control.mousePosition().addTo(map);
});
