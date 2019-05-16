#............................................
#. Syntheon control module
#. Hannes R.
#............................................

import subprocess
import os
import hashlib
import json

#............................................

class Zynaddsubfx:

  def __init__(self, config):
    self.status = False
    self.effectStatus = False
    self.loadBank(config.bankPath('zynaddsubfx'))

  def getStatus(self):
    return self.status

  def setStatus(self, status):
    if status == self.status:
      return # no action
    cmd = 'start' if status else 'stop'
    rc = subprocess.call(['systemctl', cmd, 'zynaddsubfx'])
    if rc != 0:
      raise RuntimeError('could not %s zynaddsubfx' % cmd)
    self.status = status

  def getEffectStatus(self):
    return self.effectStatus

  def setEffectStatus(self, status):
    if status == self.effectStatus:
      return # no action
    to_conn = 'rakarrack:in' if status else 'system:playback'
    to_disc = 'system:playback' if status else 'rakarrack:in'
    rc1 = subprocess.call(['/usr/bin/jack_disconnect', 'zynaddsubfx:out_1', to_disc+'_1'])
    rc2 = subprocess.call(['/usr/bin/jack_disconnect', 'zynaddsubfx:out_2', to_disc+'_2'])
    rc3 = subprocess.call(['/usr/bin/jack_connect', 'zynaddsubfx:out_1', to_conn+'_1'])
    rc4 = subprocess.call(['/usr/bin/jack_connect', 'zynaddsubfx:out_2', to_conn+'_2'])
    if rc1 != 0 or rc2 != 0 or rc3 != 0 or rc4 != 0:
      raise RuntimeError('could not connect zynaddsubfx audio')
    self.effectStatus = status

  def loadBank(self, bankPath):
    print("... Zynaddsubfx: reading bank");
    bank = [None] * 64
    for f in os.listdir(bankPath):
      entry = f.strip().split('-',1)
      bank[int(entry[0])] = entry[1].replace('.xiz','')
    bank.pop(0) # index 0 is empty
    while bank[-1] is None:
       bank.pop()
    print("... bank is now: "+str(bank))
    self.bank = bank

  def serializeBank(self):
    return json.dumps(self.bank)

  def bankChecksum(self):
    return hashlib.md5(str(self.bank)).hexdigest()[0:20]
