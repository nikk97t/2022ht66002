const mapid = "mapview1";
var map;
function load_map_data() {

  map = L.map(mapid);

  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18
  }).addTo(map);

  map.setView([12.978707, 77.601192], 17);

  return;
}

function load_nodes() {
  $.ajax({
    url: "/get_points_list",
    type: 'GET',
    dataType: 'json', // added data type
    success: function(res) {
      let nodes = res.data
      let html_gen = "";
      for (const nodeid in nodes) {
        if (nodes[nodeid]["name"] !== "unknown")
          html_gen = html_gen + "<option value='" + nodeid + "'>" + nodes[nodeid]["name"] + "</option>"
      }
      $("#from").html(html_gen)
      $("#to").html(html_gen)
    }
  });
}

var polyline_route;
function get_direction() {
  from_id = $("#from").val()
  to_id = $("#to").val()
  let link="/get_direction/" + from_id + "/" + to_id
  $("#status").html("<a href='" + link + "' target='_blank'>Open resp data</a>");

  $.ajax({
    url: "/get_direction/" + from_id + "/" + to_id,
    type: 'GET',
    dataType: 'json', // added data type
    success: function(res) {
      try {
        // polyline_route.clearLayers();
        map.removeLayer(polyline_route)
      } catch (error) {
      }
      polyline_route = L.polyline(res.data).addTo(map);
      // map.panTo(new L.LatLng(res.data[0][0], res.data[0][1]));
      console.log(res.data);
    },
    error: function(err) {
      $("#status").html("Path not found!")
    }
  });
}

load_map_data()
load_nodes()