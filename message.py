class Message():
    def __init__(self, player, onoff, tick, note, velocity):
        self._player = player
        self._onoff = onoff
        self._tick = tick
        self._note = note
        self._velocity = velocity
    def printself(self):
        print([self._tick,self._note._notename,self._velocity])
