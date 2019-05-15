#............................................
#. Syntheon control module
#. Hannes R.
#............................................

import subprocess

#............................................

class Zynaddsubfx:

  def __init__(self, config):
    self.status = False
    self.effectStatus = False

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
