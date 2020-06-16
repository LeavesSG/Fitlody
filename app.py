from channel import Channel
from player import Player
from notebook import NoteBook
from message import Message
import time
import serial
import numpy as np
import os
import sys
import tty, termios

class App():
    def __init__(self, ifarduino, address = "/dev/cu.usbmodem142101"):
        self._tickes = 0
        self._hit = False
        self._hit_count = 0
        self._hit_begin = 0
        self._hitRecord = []
        self._channel = Channel()
        self._notebook = NoteBook()
        self._player1 = Player("tempo",self._notebook)
        self._player2 = Player("chord",self._notebook)
        self._player3 = Player("melody",self._notebook)
        self.quit = False


        self._Arduino = ifarduino
        #self._Arduino = True

        if self._Arduino:
            self._serialPort = address
            self._baudRate = 9600
            self._server = serial.Serial(self._serialPort, self._baudRate, timeout=1)

    def convertData(self, data):
        decode_data = data.decode()
        result = ""
        for char in decode_data:
            if 48 <= ord(char) <= 57:
                result += char
        if len(result) > 0:
            returnvalue = int(result)
        else:
            returnvalue = 0
        return returnvalue


    def setchord(self, chordserial):
        self._chordserial = chordserial

    def chordcontrol(self):
        self._chordcount = (self._hit_count-9)//4
        chordnum = self._chordcount%8
        return self._chordserial[chordnum].get_notes()

    def currentChord(self):
        self._chordcount = (self._hit_count-9)//4
        chordnum = self._chordcount%8
        return self._chordserial[chordnum].get_name()

    def hitControl(self):
        if self._serial>100:
            if self._hit == False:
                self._hit_count += 1
                self._hitRecord.append(self._tickes)
                self._hit_begin = self._tickes
                self._hit = True

        elif self._serial <100:
            if self._hit == True:
                self._hit = False

    def messagecontrol(self):
        removelist = []

        for msg in self._channel._messages:
            if msg._tick == self._tickes:
                if msg._onoff:
                    msg._player.play_note_start(msg._note, msg._velocity)
                    removelist.append(msg)
                else:
                    msg._player.play_note_end(msg._note)
                    removelist.append(msg)
        
        for msg in removelist:
            self._channel._messages.remove(msg)


    def get_interval(self):
        intervals = [self._hitRecord[-1]-self._hitRecord[-2], self._hitRecord[-2]-self._hitRecord[-3],self._hitRecord[-3]-self._hitRecord[-4]]
        return np.mean(intervals)

    
    def basicTempo(self,velocity):
        hitinterval = self.get_interval()
        num = self._hit_count % 4
        if num%4 == 1:
            note2play = self.chordcontrol()[0]
        elif num%4 == 2:
            note2play = self.chordcontrol()[1]
        elif num%4 == 3:
            note2play = self.chordcontrol()[0]
        else:
            note2play = self.chordcontrol()[1]
        self._note2play = note2play

        if self._hit_count > 2:
            msg_on = Message(self._player1,True,self._hit_begin, note2play, velocity*1)
            self._channel.msg_get(msg_on)
            self._hit_end = self._hit_begin + int(0.1*hitinterval)
            msg_off = Message(self._player1,False ,self._hit_end, note2play, 0)
            self._channel.msg_get(msg_off)
        
        if self._hit_count > 2:
            if num%4 == 3:
                double_start = self._hit_end+int(0.4*hitinterval)
                double_end = self._hit_end+(0.5*hitinterval)
                msg_double_on = Message(self._player3, True, double_start, note2play, velocity*0.8)
                self._channel.msg_get(msg_double_on)
                msg_double_off = Message(self._player3, False, double_end , note2play, 0)
                self._channel.msg_get(msg_double_off)
    
    def basicChord(self,velocity):
        hitinterval = self.get_interval()
        num = self._hit_count % 4
        if num%4 == 1:
            note2play = self.chordcontrol()[3]
            note2play2 = self.chordcontrol()[4]
            note2play3 = self.chordcontrol()[2]
        elif num%4 == 2:
            note2play = self.chordcontrol()[2]
            note2play2 = False
        elif num%4 == 3:
            note2play = self.chordcontrol()[3]
            note2play2 = self.chordcontrol()[4]
            note2play3 = self.chordcontrol()[2]
        else:
            note2play = self.chordcontrol()[2]
            note2play2 = False
        
        if self._hit_count > 2:
            if note2play2 != False:
                msg_on = Message(self._player2,True, self._hit_begin, note2play, velocity)
                self._channel.msg_get(msg_on)
                self._hit_end = self._hit_begin + int(0.5*hitinterval)
                msg_off = Message(self._player2,False, self._hit_end, note2play,0)
                self._channel.msg_get(msg_off)
                msg2_on = Message(self._player2,True, self._hit_begin,note2play2,velocity)
                self._channel.msg_get(msg2_on)
                msg2_off = Message(self._player2,False, self._hit_begin+int(0.5*hitinterval), note2play2,0)
                self._channel.msg_get(msg2_off)
                msg3_on = Message(self._player2,True, self._hit_begin,note2play3,velocity)
                self._channel.msg_get(msg3_on)
                msg3_off = Message(self._player2,False, self._hit_begin+int(0.8*hitinterval), note2play3,0)
                self._channel.msg_get(msg3_off)
            else:
                msg_on = Message(self._player2, True, self._hit_begin, note2play, velocity)
                self._channel.msg_get(msg_on)
                self._hit_end = self._hit_begin + int(0.2*hitinterval)
                msg_off = Message(self._player2,False, self._hit_end, note2play,0)
                self._channel.msg_get(msg_off)
    
    def basicChord2(self,velocity):
        hitinterval = self.get_interval()
        num = self._hit_count % 4
        if num%4 == 1:
            note2play = self.chordcontrol()[3]
            note2play2 = self.chordcontrol()[4]
            note2play3 = self.chordcontrol()[2]
        elif num%4 == 2:
            note2play = self.chordcontrol()[2]
            note2play2 = False
        elif num%4 == 3:
            note2play = self.chordcontrol()[3]
            note2play2 = self.chordcontrol()[4]
            note2play3 = self.chordcontrol()[2]
        else:
            note2play = self.chordcontrol()[2]
            note2play2 = False
        
        if self._hit_count > 2:
            if note2play2 != False:
                msg_on = Message(self._player2,True, self._hit_begin+1, note2play, velocity)
                self._channel.msg_get(msg_on)
                self._hit_end = self._hit_begin + int(1*hitinterval)
                msg_off = Message(self._player2,False, self._hit_end, note2play,0)
                self._channel.msg_get(msg_off)
                msg2_on = Message(self._player2,True, self._hit_begin+2,note2play2,velocity)
                self._channel.msg_get(msg2_on)
                msg2_off = Message(self._player2,False, self._hit_begin+int(1*hitinterval), note2play2,0)
                self._channel.msg_get(msg2_off)
                msg3_on = Message(self._player2,True, self._hit_begin,note2play3,velocity)
                self._channel.msg_get(msg3_on)
                msg3_off = Message(self._player2,False, self._hit_begin+int(1.5*hitinterval), note2play3,0)
                self._channel.msg_get(msg3_off)
            else:
                pass
 
    
    def melody(self,velocity):

        num = self._hit_count % 8
        if (self._hit_count-8)%32<16:
            note1 = self.chordcontrol()[7]
        else:
            note1 = self.chordcontrol()[8]
        
        note2 = self.chordcontrol()[6]
        note4 = note1.get_lower_note(self._notebook)
        note3 = note1.get_lower_note(self._notebook).get_lower_note(self._notebook)

        hitinterval = self.get_interval()
        if num%8 == 1 or num%8 == 5:
            msg_on = Message(self._player3, True, self._hit_begin, note1, velocity)
            msg_off = Message(self._player3, False, self._hit_begin + int(0.2* hitinterval), note1, 0)
            msg2_on = Message(self._player3, True, self._hit_begin + int(0.5*hitinterval), note2, velocity)
            msg2_off = Message(self._player3, False, self._hit_begin + int(0.7* hitinterval), note2, 0)
            msgs = [msg_on,msg_off,msg2_on,msg2_off]
            for msg in msgs:
                self._channel.msg_get(msg)
        if num%8 == 2 or num%8 == 6:
            msg_on = Message(self._player3, True, self._hit_begin, note1, velocity)
            msg_off = Message(self._player3, False, self._hit_begin + int(0.2* hitinterval), note1, 0)
            msg2_on = Message(self._player3, True, self._hit_begin + int(0.5*hitinterval), note2, velocity)
            msg2_off = Message(self._player3, False, self._hit_begin + int(0.7* hitinterval), note2, 0)
            msg3_on = Message(self._player3, True, self._hit_begin + int(0.8*hitinterval), note1, velocity)
            msg3_off = Message(self._player3, False, self._hit_begin + int(1.1* hitinterval), note1, 0)
            msgs = [msg_on,msg_off,msg2_on,msg2_off,msg3_on,msg3_off]
            for msg in msgs:
                self._channel.msg_get(msg)
        if num%8 == 3 or num%8 == 7:
            msg2_on = Message(self._player3, True, self._hit_begin + int(0.5*hitinterval), note2, velocity)
            msg2_off = Message(self._player3, False, self._hit_begin + int(0.7* hitinterval), note2, 0)
            msgs = [msg2_on,msg2_off]
            for msg in msgs:
                self._channel.msg_get(msg)
        if num%8 == 0:
            msg_on = Message(self._player3, True, self._hit_begin, note1, velocity)
            msg_off = Message(self._player3, False, self._hit_begin + int(0.2* hitinterval), note1, 0)
            msg2_on = Message(self._player3, True, self._hit_begin + int(0.5*hitinterval), note3, velocity)
            msg2_off = Message(self._player3, False, self._hit_begin + int(0.7* hitinterval), note3, 0)
            msgs = [msg_on,msg_off,msg2_on,msg2_off]
            for msg in msgs:
                self._channel.msg_get(msg)
        if num%8 == 4:
            msg_on = Message(self._player3, True, self._hit_begin, note1, velocity)
            msg_off = Message(self._player3, False, self._hit_begin + int(0.2* hitinterval), note1, 0)
            msg2_on = Message(self._player3, True, self._hit_begin + int(0.5*hitinterval), note3, velocity)
            msg2_off = Message(self._player3, False, self._hit_begin + int(0.6* hitinterval), note3, 0)
            msg3_on = Message(self._player3, True, self._hit_begin + int(0.7*hitinterval), note4, velocity)
            msg3_off = Message(self._player3, False, self._hit_begin + int(0.8* hitinterval), note4, 0)
            msgs = [msg_on,msg_off,msg2_on,msg2_off,msg3_on,msg3_off]
            for msg in msgs:
                self._channel.msg_get(msg)

    def melody2(self,velocity):
        note1 = self.chordcontrol()[8]
        note2 = self.chordcontrol()[6]
        note3 = self.chordcontrol()[5]
        hitinterval = self.get_interval()

        msg_on = Message(self._player3, True, self._hit_begin, note1, velocity)
        msg_off = Message(self._player3, False, self._hit_begin + int(0.2* hitinterval), note1, 0)
        msg2_on = Message(self._player3, True, self._hit_begin + int((1/3)*hitinterval), note2, velocity)
        msg2_off = Message(self._player3, False, self._hit_begin + int(0.53333* hitinterval), note2, 0)
        msg3_on = Message(self._player3, True, self._hit_begin + int((2/3)*hitinterval), note3, velocity)
        msg3_off = Message(self._player3, False, self._hit_begin + int((5/6)* hitinterval), note3, 0)
        msgs = [msg_on,msg_off,msg2_on,msg2_off,msg3_on,msg3_off]
        for msg in msgs:
            self._channel.msg_get(msg)

    def appRun(self):
        if self._Arduino:
            data = self._server.readline()
            result = self.convertData(data)
            self._serial = result
        else:
            if (self._hit_count-8)%96 <32:
                self.setchord(self._notebook._Chords_Christ)
            elif (self._hit_count-8)%96 <64:
                self.setchord(self._notebook._Chords_Kanon)
            else:
                self.setchord(self._notebook._Chords_Blues)


        if self._tickes % 10 < 3:
            self._serial  = 520
        else:
            self._serial = 0
        
        self.hitControl()

        if self._tickes == self._hit_begin:
            if self._hit_count>8:
                self.basicTempo(90)
            if self._hit_count > 24:
                if (self._hit_count-8)%32 < 16:
                    self.basicChord(90)
                else:
                    self.basicChord2(90)
            if self._hit_count > 40:
                if (self._hit_count-8)%64 < 32:
                    self.melody2(100)
                else:
                    self.melody(100)
        
        self.messagecontrol()
        self.keyboard_input()

    def keyboard_input(self):
        self.fd = sys.stdin.fileno()
        self.old_settings=termios.tcgetattr(self.fd)
        try:
            tty.setraw(self.fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
        if ch=="q":
            self.quit = True
