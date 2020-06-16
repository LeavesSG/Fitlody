class Note():
    
    def __init__(self, notenum, notename):
        self._notename = notename
        self._notenum = notenum

    def get_note_number(self):
        return self._notenum

    def get_note_name(self):
        return self._notename

    def get_lower_note(self, notebook):
        self._index = notebook.get_all_notes().index(self)
        if self._index == 0:
            return None
        else:
            return notebook.get_all_notes()[self._index -1]

    def get_higher_note(self, notebook):
        self._index = notebook.get_all_notes().index(self)
        if self._index > len(notebook.get_all_notes)+1:
            return None
        else:
            return notebook.get_all_notes()[self._index + 1]
