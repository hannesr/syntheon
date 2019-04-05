#............................................
#. Syntheon control module
#. Hannes R.
#............................................

from pybleno import Characteristic
import array
from Midi import *
from ZynAdSubFx import *


zynService = Zynaddsubfx()

#............................................
class ZnOnOff(Characteristic):

  def __init__(self, uuid):
    Characteristic.__init__(self, {
      'uuid': uuid,
      'properties': ['read', 'write'],
      'value': None
    })

  def onReadRequest(self, offset, callback):
    print('... ZnOnOff - onReadRequest')
    value = 1 if zynService.getStatus() else 0
    data = array.array('B', [value])
    callback(Characteristic.RESULT_SUCCESS, data)

  def onWriteRequest(self, data, offset, withoutResponse, callback):
    try:
      print('... ZnOnOff - onWriteRequest '+str(data[0]))
      zynService.setStatus(bool(data[0]))
      if bool(data[0]):
        zynMidi = Midi('zynaddsubfx')
        zynMidi.programChange(0, 1)
      callback(Characteristic.RESULT_SUCCESS)
    except Exception as ex:
      print('... ZnOnOff: something wrong')
      print(ex)
      callback(Characteristic.RESULT_UNLIKELY_ERROR)

#............................................
class ZnEffect(Characteristic):
  def __init__(self, uuid):
    Characteristic.__init__(self, {
      'uuid': uuid,
      'properties': ['read', 'write'],
      'value': None
    })

  def onReadRequest(self, offset, callback):
    print('... ZnEffect - onReadRequest')
    value = 1 if zynService.getEffectStatus() else 0
    data = array.array('B', [value])
    callback(Characteristic.RESULT_SUCCESS, data)

  def onWriteRequest(self, data, offset, withoutResponse, callback):
    try:
      print('... ZnEffect - onWriteRequest '+str(data[0]))
      zynService.setEffectStatus(bool(data[0]))
      callback(Characteristic.RESULT_SUCCESS)
    except Exception as ex:
      print('... write preset: something wrong')
      print(ex)
      callback(Characteristic.RESULT_UNLIKELY_ERROR)

  def store(self, preset):
    self.preset = int(preset)
    self.value = array.array('B', [self.preset])
