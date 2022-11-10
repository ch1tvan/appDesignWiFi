from datetime import datetime
from PyQt5.QtCore import pyqtSignal, QThread


class timerInterrupt(QThread):

    def __init__(self):
        super().__init__()
        self.prevTime = datetime.now()

    def change_hour(self):
        while True:
            # currHour = datetime.datetime.now().hour
            currTime = datetime.now()
            if currTime.hour is not self.prevTime.hour:
                self.prevTime = currTime
                return True
            else:
                return False
