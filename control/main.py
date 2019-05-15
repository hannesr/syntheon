#!/usr/bin/python
#............................................
#. Syntheon control module
#. Hannes R.
#............................................

from pybleno import *
import sys
import platform
import signal
from RkCharacteristic import *
from ZnCharacteristic import *

#............................................

SERVICE     = '989e'

bleno = Bleno()

def onStateChange(state):
  print('... onStateChange: ' + state);
  if (state == 'poweredOn'):
    bleno.startAdvertising(platform.node(), [SERVICE])
  else:
    bleno.stopAdvertising();


def onAdvertisingStart(error):
  print('... onAdvertisingStart: ' + ('error ' + error if error else 'success'));
  if not error:
    bleno.setServices([
      BlenoPrimaryService({
        'uuid': SERVICE,
        'characteristics': [
          RkBankChecksum(),
          RkBank(),
          RkState(),
          RkPreset(),
          RkControlList(),
          RkControl(),
          ZnServiceOn(),
          ZnEffectOn(),
          ZnControlList(),
          ZnControl()
        ]
      })
    ])

bleno.on('stateChange', onStateChange)
bleno.on('advertisingStart', onAdvertisingStart)

bleno.start()
signal.pause()

bleno.stopAdvertising()
bleno.disconnect()

print('... terminated.')
sys.exit(0)
