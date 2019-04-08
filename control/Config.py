#............................................
#. Syntheon control module
#. Hannes R.
#............................................

import yaml

SCALE_MAX=127
SCALE_MIN=1

class Config:
  def __init__(self):
    try:
      load()
    except yaml.YAMLError as ex:
      print("Configuration error: "+str(ex));
      makeDefault();

  def load(self):
    with open("/opt/syntheon/data/syntheon.yaml", "r") as stream:
      self.config = yaml.safe_load(stream)

  def makeDefault(self):
    self.config = {"effects": []}

  def serializeControlTitleList(self):
    controls = []
    for c in self.config["rakarrack"]["controls"]:
      controls.append(c["title"])
    return json.dumps(controls)

  def getRakarrackControl(self, ix):
    return self.config["rakarrack"]["controls"][ix]["cc"]

  def getRakarrackScaledValue(self, ix, value):
    # for now, scales everything in 0-100 ==> 1-127
    return value*(SCALE_MAX-SCALE_MIN)/100+1
