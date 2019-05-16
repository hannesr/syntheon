#............................................
#. Syntheon control module
#. Hannes R.
#............................................

import yaml
import json

SCALE_MAX=127
SCALE_MIN=1

class Config:
  def __init__(self):
    try:
      self.load()
    except yaml.YAMLError as ex:
      print("Configuration error: "+str(ex));
      makeDefault();

  def load(self):
    with open("/opt/syntheon/data/syntheon.yaml", "r") as stream:
      self.config = yaml.safe_load(stream)

  def makeDefault(self):
    self.config = {"effects": []}

  def bankPath(self, program):
    return self.config[program]["bank"]

  def serializeControlTitleList(self, program):
    controls = []
    try:
      for c in self.config[program]["controls"]:
        controls.append(c["title"])
    except Exception as ex:
      print('... Config: bad section '+program)
    return json.dumps(controls)

  def getControl(self, program, ix):
    return self.config[program]["controls"][ix]["cc"]

  def getScaledValue(self, program, ix, value):
    # for now, scales everything in 0-100 ==> 1-127
    # consider having a separate scale for each confirurable section
    # or perhaps a default scale 1-127, and possibility to override it
    # for each control individually
    return value*(SCALE_MAX-SCALE_MIN)/100+1
