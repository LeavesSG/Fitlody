from app import App
import time


if __name__ == "__main__":
    while True:
        x = input("do you want to use Arduino as input [y/n]: ")
        if x == "y":
            y = input("please paste your arduino port address here: ")
            ifarduino = True
            break
        else:
            ifarduino = False
            y = None
            break
        
    App1 = App(ifarduino, y)
    while True:
        App1._tickes += 1
        time.sleep(0.090)
        if App1.quit == False:
            App1.appRun()
        else:
            App1._player1.close()
            App1._player2.close()
            App1._player3.close()
            break