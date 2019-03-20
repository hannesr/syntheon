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

#............................................

SERVICE     = '989e'
RK_BANK_CS  = '9b43'
RK_BANK     = '9b96'
RK_PRESET   = '9d12'

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
          RkBankChecksum(RK_BANK_CS),
          RkBank(RK_BANK),
          RkPreset(RK_PRESET)
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


