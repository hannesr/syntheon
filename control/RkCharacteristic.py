#............................................
#. Syntheon control module
#. Hannes R.
#............................................

from pybleno import Characteristic
import array
from Midi import *
from Rakarrack import *


rakarrackBank = Rakarrack()
rakarrackMidi = Midi('rakarrack')

# see http://rakarrack.sourceforge.net/midiic.html
CTL_REVERB = 57
CTL_TOGGLE = 116
VAL_FX = 124


#............................................
class RkBank(Characteristic):

  def __init__(self, uuid):
    Characteristic.__init__(self, {
      'uuid': uuid,
      'properties': ['read'],
      'value': None
    })

  def onReadRequest(self, offset, callback):
    print('... RkBank - onReadRequest, offset=%d' % offset)
    data = array.array('B', rakarrackBank.serialize())
    print("... resp data is: "+str(data[offset:]))
    callback(Characteristic.RESULT_SUCCESS, data[offset:])

#............................................
class RkBankChecksum(Characteristic):

  def __init__(self, uuid):
    Characteristic.__init__(self, {
      'uuid': uuid,
      'properties': ['read'],
      'value': None
    })

  def onReadRequest(self, offset, callback):
    print('... RkBankChecksum - onReadRequest')
    data = array.array('B', rakarrackBank.checksum())
    callback(Characteristic.RESULT_SUCCESS, data)

#............................................
class RkPreset(Characteristic):
  def __init__(self, uuid):
    Characteristic.__init__(self, {
      'uuid': uuid,
      'properties': ['read', 'write', 'notify'],
      'value': None
    })
    self.store(0)

  def onReadRequest(self, offset, callback):
    print('... RkPreset - onReadRequest')
    callback(Characteristic.RESULT_SUCCESS, self.value)

  def onWriteRequest(self, data, offset, withoutResponse, callback):
    print('... RkPreset - onWriteRequest')
    try:
      preset = data[0]
      if self.preset == preset:
        print('... preset no change')
        pass
      elif self.preset == 0 and preset > 0:
        print('... preset on and set to %d' % preset)
        rakarrackMidi.controlChange(0, CTL_TOGGLE, VAL_FX)
        rakarrackMidi.programChange(0, int(preset))
      elif self.preset > 0 and preset == 0:
        print('... preset off')
        rakarrackMidi.controlChange(0, CTL_TOGGLE, VAL_FX)
      else:
        print('... preset set to %d' % preset)
        rakarrackMidi.programChange(0, int(preset))
      self.store(preset)
      callback(Characteristic.RESULT_SUCCESS)
    except Exception as ex:
      print('... write preset: something wrong')
      print(ex)
      callback(Characteristic.RESULT_UNLIKELY_ERROR)

  def store(self, preset):
    self.preset = int(preset)
    self.value = array.array('B', [self.preset])
