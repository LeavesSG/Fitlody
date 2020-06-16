from note import Note
from chord import Chord

class NoteBook:
    def __init__(self):
        self._Notenames = ["c2","c2s","d2","d2s","e2","f2","f2s","g2","g2s","a2","a2s","b2","c3","c3s","d3","d3s","e3","f3","f3s","g3","g3s","a3","a3s","b3","c4","c4s","d4","d4s","e4","f4","f4s","g4","g4s","a4","a4s","b4","c5"]
        self._Noteset = []
        self._Notedict = {}


        self.note_init()
        self.chord_init()
        
    def note_init(self):
        num = 48
        for i in self._Notenames:
            globals()[i] = Note(num,i)
            self._Notedict[i] = globals()[i]
            self._Noteset.append(self._Notedict[i])
            num += 1
    
    def get_all_notes(self):
        return self._Noteset
    
    def chord_init(self):
        global chord_C, chord_Cmaj7, chord_D7, chord_Dm7, chord_E7, chord_F, chord_Fm, chord_G, chord_Am, chord_Bdim, chord_Em 
        chord_C = Chord("C",[c2,e2,c3,e3,g3,c4,e4,g4,c5])
        chord_Cmaj7 = Chord("Cmaj7",[c2,g2,c3,e3,b3,c4,g4,b4,b4])
        chord_D7 = Chord("D7",[d2,f2s,d3,a3,c4,d4,f4s,a4,a4])
        chord_Dm7 = Chord("Dm7",[d2,f2,d3,a3,c4,d4,f4,a4,a4])
        chord_E7 = Chord("E7",[e2,g2s,e3,g3s,d4,e4,g4s,b4,b4])
        chord_F = Chord("F",[f2,a2,c3,f3,a3,c4,f4,a4,a4])
        chord_Fm = Chord("Fm",[f2,g2s,f3,g3s,c4,f4,g4s,c5,c5])
        chord_G = Chord("G",[g2,b2,d3,g3,b3,d4,g4,b4,b4])
        chord_Am = Chord("Am",[a2,c3,e3,a3,c4,e4,a4,c5,c5])
        chord_Bdim = Chord("Bdim",[b2,f2,d3,f3,b3,d4,f4,b4,b4])
        chord_Em = Chord("Em",[e2,g2,e3,g3,b3,e4,g4,b4,b4])
        self._chords = [chord_C, chord_Cmaj7, chord_D7, chord_Dm7, chord_E7, chord_F, chord_Fm, chord_G, chord_Am, chord_Bdim, chord_Em ]


        self._Chords_Kanon = [chord_C, chord_G, chord_Am, chord_Em, chord_F, chord_C, chord_F, chord_G]
        self._Chords_Blues = [chord_Cmaj7, chord_Dm7, chord_Bdim, chord_Em, chord_F, chord_Bdim, chord_E7, chord_Cmaj7]
        self._Chords_Christ = [chord_Am, chord_Em, chord_F,chord_E7,chord_Am,chord_F,chord_Fm,chord_C]
        
        self._chord_progressions = [self._Chords_Blues, self._Chords_Christ, self._Chords_Kanon]
    
    def get_all_chords(self):
        return self._chords

    def get_chord_progressions(self):
        return self._chord_progressions

notebook = NoteBook()
for i in notebook.get_all_notes():
    print(i.get_note_number())