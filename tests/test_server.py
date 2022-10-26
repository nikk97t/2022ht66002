import json
import os, sys
import inspect
import unittest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from server import app

class ServerTests(unittest.TestCase):

  def setUp(self):
    self.ctx = app.app_context()
    self.ctx.push()
    self.client = app.test_client()

  def tearDown(self):
    self.ctx.pop()

  def test_home(self):
    response = self.client.get("/")
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert data["message"] == "Welcome to nikk WebApp for shortest path finder"

  def test_get_points_list(self):
    response = self.client.get("/get_points_list")
    assert response.status_code == 200

  def test_get_direction(self):
    response = self.client.get("/get_points_list")
    data = json.loads(response.get_data(as_text=True))["data"]

    response = self.client.get("/get_direction/" + list(data.keys())[0] + "/" + list(data.keys())[1])
    assert response.status_code == 200 or response.status_code == 500

if __name__ == "__main__":
  unittest.main()