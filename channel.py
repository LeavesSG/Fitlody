class Channel():
    def __init__(self):

        self._messages = []
    
    def msg_get(self, msg):
        self._messages.append(msg)
    
    def msg_remove(self, msg):
        self._messages.remove(msg)
