#............................................
#. Syntheon control module
#. Hannes R.
#............................................

from pybleno import Characteristic
import array
from Midi import *
from Rakarrack import *
from Config import *

config = Config()
rakarrackService = Rakarrack(config)
rakarrackMidi = Midi('rakarrack')

# see http://rakarrack.sourceforge.net/midiic.html
CTL_REVERB = 57
CTL_TOGGLE = 116
VAL_FX = 124


#............................................
class RkBank(Characteristic):

  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': '9b96',
      'properties': ['read'],
      'value': None
    })

  def onReadRequest(self, offset, callback):
    print('... RkBank - onReadRequest, offset={}'.format(offset))
    data = array.array('B', rakarrackService.serializeBank())
    print("... resp data is: "+str(data[offset:]))
    callback(Characteristic.RESULT_SUCCESS, data[offset:])

#............................................
class RkBankChecksum(Characteristic):

  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': '9b43',
      'properties': ['read'],
      'value': None
    })

  def onReadRequest(self, offset, callback):
    print('... RkBankChecksum - onReadRequest')
    data = array.array('B', rakarrackService.bankChecksum())
    callback(Characteristic.RESULT_SUCCESS, data)

#............................................
class RkState(Characteristic):
  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': '9d10',
      'properties': ['read', 'write', 'notify'],
      'value': None
    })
    self.active = 0

  def onReadRequest(self, offset, callback):
    print('... RkState - onReadRequest')
    value = array.array('B', [self.active])
    callback(Characteristic.RESULT_SUCCESS, value)

  def onWriteRequest(self, data, offset, withoutResponse, callback):
    print('... RkState - onWriteRequest')
    try:
      active = data[0]
      if self.active == active:
        print('... RkState: no change')
      else:
        print('... RkState: {} -> {}'.format(self.active, active))
        rakarrackMidi.controlChange(0, CTL_TOGGLE, VAL_FX)
      self.active = active
      callback(Characteristic.RESULT_SUCCESS)
    except Exception as ex:
      print('... write preset: something wrong')
      print(ex)
      callback(Characteristic.RESULT_UNLIKELY_ERROR)

#............................................
class RkPreset(Characteristic):
  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': '9d12',
      'properties': ['read', 'write', 'notify'],
      'value': None
    })
    self.preset = 0

  def onReadRequest(self, offset, callback):
    print('... RkPreset - onReadRequest')
    value = array.array('B', [self.preset])
    callback(Characteristic.RESULT_SUCCESS, value)

  def onWriteRequest(self, data, offset, withoutResponse, callback):
    print('... RkPreset - onWriteRequest')
    try:
      preset = data[0]
      if self.preset == preset:
        print('... RkPreset: no change')
      else:
        print('... RkPreset: {} -> {}'.format(self.preset, preset))
        rakarrackMidi.programChange(0, int(preset)+1)
      self.preset = preset
      callback(Characteristic.RESULT_SUCCESS)
    except Exception as ex:
      print('... write preset: something wrong')
      print(ex)
      callback(Characteristic.RESULT_UNLIKELY_ERROR)

#............................................
class RkControlList(Characteristic):
  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': '9d19',
      'properties': ['read'],
      'value': None
    })

  def onReadRequest(self, offset, callback):
    print('... RkControlList - onReadRequest (offset={})'.format(offset))
    data = array.array('B', config.serializeControlTitleList("rakarrack"))
    print("... resp data is: "+str(data[offset:]))
    callback(Characteristic.RESULT_SUCCESS, data[offset:])

#............................................
class RkControl(Characteristic):
  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': '9d1a',
      'properties': ['write'],
      'value': None
    })

  def onWriteRequest(self, data, offset, withoutResponse, callback):
    print('... RkControl - onWriteRequest')
    try:
      for i in range(0, len(data)-1, 2):
        ctl = config.getRakarrackControl(data[i])
        val = config.getRakarrackScaledValue(data[i], data[i+1])
        rakarrackMidi.controlChange(0, ctl, val)
      callback(Characteristic.RESULT_SUCCESS)
    except Exception as ex:
      print('... RkControl: something wrong')
      print(ex)
      callback(Characteristic.RESULT_UNLIKELY_ERROR)
