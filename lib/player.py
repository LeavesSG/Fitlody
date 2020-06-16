import rtmidi

class Player():

    def __init__(self,portname, notebook):
        self._midiout = rtmidi.MidiOut()

        self._midiout.open_virtual_port(portname)

        self._midiout.send_message([0x90,48,1])
        self._midiout.send_message([0x80,48,0])

    def play_note_start(self,note, velocity):
        self._midiout.send_message([0x90, note.get_note_number(),velocity])

    def play_note_end(self, note):
        self._midiout.send_message([0x80, note.get_note_number(),0])
    
    def close(self):
        del self._midiout
