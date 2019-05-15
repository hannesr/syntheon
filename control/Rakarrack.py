#............................................
#. Syntheon control module
#. Hannes R.
#............................................

import hashlib
import json

#............................................

class Rakarrack:

  def __init__(self):
    self.loadBank()

  def loadBank(self):
    print("... reading bank");
    bank = [None] * 64
    for row in open("/opt/syntheon/data/rakarrack-bank.log", "r"):
      entry = row.strip().split(':')
      if len(entry)==3 and entry[0]=='RKR_BANK_NAME' and len(entry[2])>0:
        bank[int(entry[1])] = entry[2]
    bank.pop(0) # index 0 is empty
    while bank[-1] is None:
       bank.pop()
    print("... bank is now: "+str(bank))
    self.bank = bank

  def serialize(self):
    return json.dumps(self.bank)

  def checksum(self):
    return hashlib.md5(str(self.bank)).hexdigest()[0:20]
