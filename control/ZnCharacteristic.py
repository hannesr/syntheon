#............................................
#. Syntheon control module
#. Hannes R.
#............................................

from pybleno import Characteristic
import array
from Midi import *
from Zynaddsubfx import *


zynService = Zynaddsubfx()
zynMidi = Midi('zynaddsubfx')

#............................................
class ZnOnOff(Characteristic):

  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': '9e01',
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
        zynMidi.reset()
        zynMidi.programChange(0, 1)
      callback(Characteristic.RESULT_SUCCESS)
    except Exception as ex:
      print('... ZnOnOff: something wrong')
      print(ex)
      callback(Characteristic.RESULT_UNLIKELY_ERROR)

#............................................
class ZnEffect(Characteristic):
  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': '9e04',
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

#............................................
class ZnControlList(Characteristic):
  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': '9e08',
      'properties': ['read'],
      'value': None
    })

  def onReadRequest(self, offset, callback):
    print('... ZnControlList - onReadRequest (offset={})'.format(offset))
    data = array.array('B', config.serializeControlTitleList("zynaddsubfx"))
    print("... resp data is: "+str(data[offset:]))
    callback(Characteristic.RESULT_SUCCESS, data[offset:])

#............................................
class ZnControls(Characteristic):
  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': '9e0a',
      'properties': ['read', 'write'],
      'value': None
    })
    self.volume = 100

  def onReadRequest(self, offset, callback):
    print('... ZnControls - onReadRequest')
    data = array.array('B', [self.volume])
    callback(Characteristic.RESULT_SUCCESS, data)

  def onWriteRequest(self, data, offset, withoutResponse, callback):
    try:
      print('... ZnControls - onWriteRequest '+str(data[0]))
      zynMidi.controlChange(0, Midi.VOLUME, )
      callback(Characteristic.RESULT_SUCCESS)
    except Exception as ex:
      print('... write preset: something wrong')
      print(ex)
      callback(Characteristic.RESULT_UNLIKELY_ERROR)
