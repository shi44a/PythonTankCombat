from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint, QTimer
import Tank as t


class STank(t.Tank):
    def __init__(self, parent, ):
        super().__init__(parent)
        self.pixmaplist = ['./img/su1', './img/su2', './img/sl1', './img/sl2', './img/sd1', './img/sd2', './img/sr1',
                       './img/sr2']

        self.isPressed = False

        self.moveTimer = QTimer(self)
        self.moveTimer.setSingleShot(False)
        self.moveTimer.timeout.connect(self.STankMove)
        self.moveTimer.start(50)

        self.isinvincible = True


    def STankMove(self):
        if self.isPressed:
            self.tankMove()


    def stop(self):
        self.moveTimer.stop()

    def start(self):
        self.moveTimer.start(50)