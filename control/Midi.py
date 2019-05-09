#............................................
#. Syntheon control module
#. Hannes R.
#............................................

import rtmidi

# https://www.midi.org/specifications-old/item/table-1-summary-of-midi-message
# https://www.midi.org/specifications-old/item/table-3-control-change-messages-data-bytes-2
#............................................

class Midi:

  def __init__(self, program):
    self.program = program
    self.reset()

  def reset(self):
    self.midi_out = rtmidi.MidiOut()
    ports = self.midi_out.get_ports()
    matching_ports = [i for i, l in enumerate(ports) if self.program in l]
    if matching_ports:
      self.midi_out.open_port(matching_ports[0])
    else:
      print("... warning: no midi connection for {}".format(self.program))
      self.midi_out.open_virtual_port('Dummy')

  def programChange(self, channel, value):
    self.midi_out.send_message([192+channel, value])

  def controlChange(self, channel, control, value):
    self.midi_out.send_message([176+channel, control, value])

  def pitchBend(self, channel, value):
    #self.midi_out.send_message([224+channel, lsb, msb])
    pass
