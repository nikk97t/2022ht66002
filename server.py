import json
import os
import os.path
from Utils.Utils1 import read_raw_data, pre_process_data, transform_data_to_mode2, point_id, json_resp
from flask import Flask, jsonify, request, send_file
from dijkstar import Graph, find_path

# read config file
config_file = "config.json"
if not os.path.exists(config_file):
  raise FileNotFoundError(config_file)

config = {}
with open(config_file, "r") as cfr:
  config = json.loads(cfr.read())

datafile = os.path.join("data", "geojson_raw.json")
# pre process the raw data
data = pre_process_data(data=read_raw_data(file=datafile)["data"])
tr_data = transform_data_to_mode2(pointsarr=data["points"])
graph = Graph()

# for point in data["points"]:
#   g.add_vertex(point["id"])

for path in data["paths"]:

  if (path["direction"].lower() == "ste" or path["direction"].lower() == "both"):
    start_coordinates = path["coordinates"][0]
    end_coordinates = path["coordinates"][-1]

    from_point = point_id(coordinate=start_coordinates, transformed_data=tr_data)
    to_point = point_id(coordinate=end_coordinates, transformed_data=tr_data)

    graph.add_edge(from_point, to_point, path["distance"])
  if (path["direction"].lower() == "ets" or path["direction"].lower() == "both"):
    start_coordinates = path["coordinates"][-1]
    end_coordinates = path["coordinates"][0]

    from_point = point_id(coordinate=start_coordinates, transformed_data=tr_data)
    to_point = point_id(coordinate=end_coordinates, transformed_data=tr_data)

    graph.add_edge(from_point, to_point, path["distance"])

print(graph.get_data())



print("-"*70)
print("-"*70)


# while(True):
#   from_id = input("id of from node")
#   to_id = input("id of from node")
#   sh = find_path(graph, from_id, to_id)
#   latlon_points = []
#   for point in sh.nodes:
#     latlon_points.append(tr_data[point])
#   print(json.dumps(latlon_points))

app = Flask(__name__, static_url_path="/webui", static_folder="ui")

@app.route('/get_points_list')
def get_points_list():
  ret_data = { "status":200, "message":"", "data":{} }

  with open(os.path.join("data", "transformed_data.json")) as tdf:
    ret_data["data"] = json.loads(tdf.read())

  return jsonify(ret_data), ret_data["status"]

@app.route('/get_direction/<fromid>/<toid>')
def get_direction(fromid, toid):
  ret_data = { "status":200, "message":"", "data":{} }

  sh = find_path(graph, fromid, toid)
  route_points = []
  for point in sh.nodes:
    ptt = [tr_data[point][1], tr_data[point][0]]
    # route_points.append(tr_data[point])
    route_points.append(ptt)

  ret_data["data"] = route_points
  return jsonify(ret_data)

@app.route('/')
def hello_world():
  ret_data = { "status":200, "message":"", "data":{} }
  ret_data["message"] = "Welcome to nikk WebApp for shortest path finder"
  ret_data["data"]["env"] = os.environ["ENVIRONMENT"]
  return jsonify(ret_data), ret_data["status"]

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=config["server"]["port"])