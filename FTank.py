from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint, QTimer
import Tank as t


class FTank(t.Tank):

    def __init__(self, parent,):
        super().__init__(parent)

        self.isPressed = False

        self.moveTimer = QTimer(self)
        self.moveTimer.setSingleShot(False)
        self.moveTimer.timeout.connect(self.FTankMove)
        self.moveTimer.start(50)

        self.isinvincible=True


    def FTankMove(self):
        if self.isPressed:
            self.tankMove()


    def stop(self):
        self.moveTimer.stop()

    def start(self):
        self.moveTimer.start(50)