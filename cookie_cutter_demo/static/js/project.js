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

      var dataurl = '/geodata/data.geojson';   
      var trackurl = '/geodata/track.geojson';   
      window.addEventListener("map:init", function (event) {
        var firstLoad = true
        var map = event.detail.map;
        // Put realtime markers on the map with a GeoJSON feed
        point_locs = L.realtime({
              url:  dataurl,
              crossOrigin: false,
              type: 'json'},
              {
                interval: 3 * 1000,
                getFeatureId: function(featureData){
                   return featureData.properties.device_id;
                }
              }).addTo(map);

          
        // Download track data too  
        point_tracks = L.realtime({
              url:  trackurl,
              crossOrigin: false,
              type: 'json'},
              {
                interval: 6 * 1000,
              }).addTo(map);     
              
        // recenter map on updates...
        point_tracks.on('update', function() {
              if (firstLoad){
                  map.fitBounds(point_tracks.getBounds());
                  firstLoad = false
                  }
              });
      });

