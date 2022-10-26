import os, sys
import inspect
import unittest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import Utils.Utils1 as Utils1


class TestUtils(unittest.TestCase):

  def test_read_raw_data_success(self):
    raw_data_file = os.path.join("data", "geojson_raw.json")
    resp_data = Utils1.read_raw_data(file=raw_data_file)
    self.assertTrue(resp_data["status"])

  def test_read_raw_data_failure(self):
    raw_data_file = os.path.join("invaliddata", "geojson_raw.json")
    self.assertRaises(FileNotFoundError, Utils1.read_raw_data, (raw_data_file))

  def test_get_distance_by_array_of_points(self):
    path_arr = [
        [
            77.60248196322306,
            12.979329194426825
        ],
        [
            77.60250842473317,
            12.979200045659852
        ],
        [
            77.60239276000368,
            12.979235394095937
        ]
    ]
    dist = Utils1.get_distance_by_array_of_points(path_arr)
    self.assertAlmostEqual(dist, 0.01715621924045622)
    
  def test_check_point_in_points(self):
    point = [1,2]
    points = [{"coordinates": [1,2]}]
    self.assertTrue(Utils1.check_point_in_points(point=point, pointsarray=points))
    self.assertFalse(Utils1.check_point_in_points(point=point, pointsarray=[]))

  def test_json_resp(self):
    testmsg = "testmsg"
    resp = Utils1.json_resp(message=testmsg)
    self.assertEqual(resp["message"], testmsg)

  def test_pre_process_data(self):
    raw_data_file = os.path.join("data", "geojson_raw.json")
    proc_data = Utils1.pre_process_data(Utils1.read_raw_data(file=raw_data_file)["data"])

    self.assertTrue(type(proc_data) is dict)

    tr_data = Utils1.transform_data_to_mode2(pointsarr=proc_data["points"])

    resp = Utils1.point_id(coordinate=[77.59752441096839,12.98096842269932], transformed_data=tr_data)

    resp = Utils1.point_id(coordinate=[1,2], transformed_data=tr_data)

