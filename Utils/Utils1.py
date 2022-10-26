import json
import uuid
import os.path
from math import sin, cos, sqrt, atan2, radians

def read_raw_data(file):
  if (os.path.exists(file)):
    with open(file, "r") as rfr:
      return {"status": True, "data": json.loads(rfr.read())}
  else:
    raise FileNotFoundError(file)

def write_processed_data(data, filename="processed_data.json"):
  with open(os.path.join("data", filename), "w") as wjd:
    json.dump(data, wjd, indent=4, sort_keys=True)

def get_distance_by_array_of_points(data_arr):
  # approximate radius of earth in km
  R = 6373.0

  total_distance = 0

  start_point = None
  end_point = None
  for point in data_arr:
    end_point = point

    # print(start_point)
    # print(end_point)
    # print("-"*10)
    if (start_point is not None):
      # calculate distance
      lat1 = radians(start_point[0])
      lon1 = radians(start_point[1])
      lat2 = radians(end_point[0])
      lon2 = radians(end_point[1])

      dlon = lon2 - lon1
      dlat = lat2 - lat1

      a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
      c = 2 * atan2(sqrt(a), sqrt(1 - a))

      local_distance = R * c

      # print("local_distance=" + str(local_distance))
      total_distance += local_distance

    start_point = end_point

  return total_distance

def check_point_in_points(point, pointsarray):
  for i_point in pointsarray:
    if sorted(point) == sorted(i_point["coordinates"]):
      return True
  return False

def json_resp(status=200, message="", data={}):
  return {
    "status": status,
    "message": message,
    "data": data
  }



def pre_process_data(data):
  # pre check if any required feature missing
  for feature in data["features"]:
    if feature["geometry"]["type"] == "point" and "name" not in feature["properties"]:
      raise ValueError(feature)
    # elif feature["geometry"]["type"] == "LineString" and "name" not in feature["properties"]:
    #   print("name key not present in linestring")
    #   raise ValueError(feature)
    elif feature["geometry"]["type"] == "LineString" and "direction" not in feature["properties"]:
      print("direction key not present in linestring")
      raise ValueError(feature)

  # collect points and populate distances
  processed_data_1 = {"points": [], "paths": []}
  for feature in data["features"]:
    if feature["geometry"]["type"] == "Point":
      processed_data_1["points"].append({
        "coordinates": feature["geometry"]["coordinates"],
        "name": feature["properties"]["name"],
        "id": uuid.uuid4().hex
      })
    elif feature["geometry"]["type"] == "LineString":
      processed_data_1["paths"].append({
        "coordinates": feature["geometry"]["coordinates"],
        "name": feature["properties"]["name"] if "name" in feature["properties"] else "unknown",
        "direction": feature["properties"]["direction"],
        "distance": round(get_distance_by_array_of_points(data_arr=feature["geometry"]["coordinates"])*1000)
      })

  # extract points from routes
  for path in processed_data_1["paths"]:
    if (not check_point_in_points(point=path["coordinates"][0], pointsarray=processed_data_1["points"])):
      processed_data_1["points"].append({
        "coordinates": path["coordinates"][0],
        # "name": feature["properties"]["name"],
        "id": uuid.uuid4().hex
      })
    if (not check_point_in_points(point=path["coordinates"][-1], pointsarray=processed_data_1["points"])):
      processed_data_1["points"].append({
        "coordinates": path["coordinates"][-1],
        # "name": feature["properties"]["name"],
        "id": uuid.uuid4().hex
      })

  write_processed_data(data=processed_data_1)
  return processed_data_1


def transform_data_to_mode2(pointsarr):
  data = {}
  detailed_data = {}
  for point in pointsarr:
    data[point["id"]] = point["coordinates"]
    detailed_data[point["id"]] = {
      "coordinates": point["coordinates"],
      "name": point["name"] if "name" in point else "unknown"
    }

  write_processed_data(data=detailed_data, filename="transformed_data.json")
  return data

def point_id(coordinate, transformed_data):
  for pointid in transformed_data:
    if (set(coordinate) == set(transformed_data[pointid])):
      return pointid

