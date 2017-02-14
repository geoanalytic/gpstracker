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
		
    var wmsLayer = L.tileLayer.betterWms('https://webmap.positionbot.com//mapserv/?map=/data/mapfiles/didsplus/didsplus.map&', {
		layers: 'DIDsPlus',
		format: 'image/png',
		transparent: true,
		attribution: "AltaLis"
    });  //.addTo(map);
//	wmsLayer.setZIndex(399);
	
	map.layerscontrol.addOverlay(wmsLayer, "DIDs+");
	
	
	var tmsCadastral = L.tileLayer('https://webmap.positionbot.com/mapcache/tms/1.0.0/Cadastral@g21/{z}/{x}/{y}.png', {
        tms: true,
		maxZoom: 21,
		attribution: 'Data from <a href="http://altalis.com">AltaLIS</a>'
	});
//('Cadastral',      'https://webmap.positionbot.com/mapcache/tms/1.0.0/Cadastral@g21/{z}/{x}/{y}.png', {'attribution': 'Data from <a href="http://altalis.com">AltaLIS</a>','maxZoom': 21, 'tms': 'true' }),	
	map.layerscontrol.addOverlay(tmsCadastral, "Cadastral");
	
	
//	var topPane = map._createPane('leaflet-top-pane', map.getPanes().mapPane);
//	topPane.appendChild(wmsLayer.getContainer());
	
    L.control.mousePosition().addTo(map);
});
