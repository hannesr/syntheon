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
RK_BANK_CS  = '9b43'
RK_BANK     = '9b96'
RK_PRESET   = '9d12'
RK_EFFECT_LIST  = '9d19'
RK_EFFECT   = '9d1a'
ZN_ONOFF    = '9e01'
ZN_EFFECT   = '9e04'

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
          RkPreset(RK_PRESET),
          RkEffectList(RK_EFFECT_LIST),
          RkEffect(RK_EFFECT),
          ZnOnOff(ZN_ONOFF),
          ZnEffect(ZN_EFFECT)
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
