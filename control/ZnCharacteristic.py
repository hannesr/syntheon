#............................................
#. Syntheon control module
#. Hannes R.
#............................................

from pybleno import Characteristic
import array
from Midi import *
from Zynaddsubfx import *
from Config import *

config = Config()
zynService = Zynaddsubfx(config)
zynMidi = Midi('zynaddsubfx')

#............................................
class ZnBank(Characteristic):

  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': '9e14',
      'properties': ['read'],
      'value': None
    })

  def onReadRequest(self, offset, callback):
    print('... ZnBank - onReadRequest, offset={}'.format(offset))
    data = array.array('B', zynService.serializeBank())
    print("... resp data is: "+str(data[offset:]))
    callback(Characteristic.RESULT_SUCCESS, data[offset:])

#............................................
class ZnBankChecksum(Characteristic):

  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': '9e12',
      'properties': ['read'],
      'value': None
    })

  def onReadRequest(self, offset, callback):
    print('... ZnBankChecksum - onReadRequest')
    data = array.array('B', zynService.bankChecksum())
    callback(Characteristic.RESULT_SUCCESS, data)

#............................................
class ZnServiceState(Characteristic):

  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': '9e01',
      'properties': ['read', 'write'],
      'value': None
    })

  def onReadRequest(self, offset, callback):
    print('... ZnServiceState - onReadRequest')
    value = 1 if zynService.getStatus() else 0
    data = array.array('B', [value])
    callback(Characteristic.RESULT_SUCCESS, data)

  def onWriteRequest(self, data, offset, withoutResponse, callback):
    try:
      print('... ZnServiceState - onWriteRequest '+str(data[0]))
      zynService.setStatus(bool(data[0]))
      if bool(data[0]):
        zynMidi.reset()
        zynMidi.programChange(0, 1)
      callback(Characteristic.RESULT_SUCCESS)
    except Exception as ex:
      print('... ZnServiceState: something wrong')
      print(ex)
      callback(Characteristic.RESULT_UNLIKELY_ERROR)

#............................................
class ZnEffectState(Characteristic):
  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': '9e04',
      'properties': ['read', 'write'],
      'value': None
    })

  def onReadRequest(self, offset, callback):
    print('... ZnEffectState - onReadRequest')
    value = 1 if zynService.getEffectStatus() else 0
    data = array.array('B', [value])
    callback(Characteristic.RESULT_SUCCESS, data)

  def onWriteRequest(self, data, offset, withoutResponse, callback):
    try:
      print('... ZnEffectState - onWriteRequest '+str(data[0]))
      zynService.setEffectStatus(bool(data[0]))
      callback(Characteristic.RESULT_SUCCESS)
    except Exception as ex:
      print('... ZnEffectState: something wrong')
      print(ex)
      callback(Characteristic.RESULT_UNLIKELY_ERROR)

#............................................
class ZnPreset(Characteristic):
  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': '9e17',
      'properties': ['write'],
      'value': None
    })

  def onWriteRequest(self, data, offset, withoutResponse, callback):
    print('... ZnPreset - onWriteRequest')
    try:
      preset = data[0]
      zynMidi.programChange(0, int(preset))
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
class ZnControl(Characteristic):
  def __init__(self):
    Characteristic.__init__(self, {
      'uuid': '9e0a',
      'properties': ['write'],
      'value': None
    })

  def onWriteRequest(self, data, offset, withoutResponse, callback):
    print('... ZnControl - onWriteRequest')
    try:
      for i in range(0, len(data)-1, 2):
        ctl = config.getControl("zynaddsubfx", data[i])
        val = config.getScaledValue("zynaddsubfx", data[i], data[i+1])
        zynMidi.controlChange(0, ctl, val)
      callback(Characteristic.RESULT_SUCCESS)
    except Exception as ex:
      print('... ZnControl: something wrong')
      print(ex)
      callback(Characteristic.RESULT_UNLIKELY_ERROR)
