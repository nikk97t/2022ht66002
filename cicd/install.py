import json
import os

config = {}
with open("config.json", "r") as cjrd:
  config = json.loads(cjrd.read())

config["server"]["port"] = os.environ["PORT"]
config["server"]["environment"] = os.environ["ENVIRONMENT"]

with open("config.json", "w") as cjwd:
  json.dump(config, cjwd, indent=4, sort_keys=False)