class Chord():

    def __init__(self,name,notes):
        self._notes = notes
        self._base = notes[0]
        self._name = name
    
    def note_included(self, note):
        included = False
        for i in self._notes:
            if i.get_note_number() == note.get_note_number():
                included = True
        return included
    
    def get_notes(self):
        return self._notes
        

    def get_name(self):
        return self._name
