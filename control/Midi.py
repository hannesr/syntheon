#............................................
#. Syntheon control module
#. Hannes R.
#............................................

import rtmidi

#............................................

class Midi:

  def __init__(self, program):
    self.midi_out = rtmidi.MidiOut()
    ports = self.midi_out.get_ports()
    matching_ports = [i for i, l in enumerate(ports) if program in l]
    if matching_ports:
      self.midi_out.open_port(matching_ports[0])
    else:
      self.midi_out.open_virtual_port('Dummy')

  def programChange(self, channel, value):
    self.midi_out.send_message([192+channel, value])

  def controlChange(self, channel, control, value):
    self.midi_out.send_message([176+channel, control, value])

  def pitchBend(self, channel, value):
    #self.midi_out.send_message([224+channel, lsb, msb])
    pass
