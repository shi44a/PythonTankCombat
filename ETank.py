from PyQt5.QtCore import Qt, QPoint, QTimer
import Tank as t
import random


class ETank(t.Tank):

    def __init__(self, parent, ):
        super().__init__(parent)
        self.pixmaplist = ['./img/eu1', './img/eu2', './img/el1', './img/el2', './img/ed1', './img/ed2', './img/er1',
                           './img/er2']
        self.direction = 'd'

        self.actionTimer = QTimer(self)
        self.actionTimer.timeout.connect(self.ETankAction)
        self.actionTimer.start(50)

        self.moveTimer = QTimer(self)
        self.moveTimer.timeout.connect(self.moveChange)
        self.moveTimer.start(400)

        self.fireTimer = QTimer(self)
        self.fireTimer.timeout.connect(self.fireChange)
        self.fireTimer.start(500)

        self.fire = False


    def moveChange(self):
        move = random.randint(0, 5) % 5
        if move == 0:
            self.isMoving=False
            return
        else:
            if move == 1:
                self.direction = 'u'
            elif move == 2:
                self.direction = 'd'
            elif move == 3:
                self.direction = 'l'
            elif move == 4:
                self.direction = 'r'


    def fireChange(self):
        fire=random.randint(0, 2) % 2
        if fire==0:
            self.fire=False
        else:
            self.fire=True

    def ETankAction(self):
        if self.isHited is False:
            self.tankMove()
            self.isMoving = True
            if self.fire is True:
                self.tankFire()
                self.fire = False
        else:
            return

    def stop(self):
        self.actionTimer.stop()

    def start(self):
        self.actionTimer.start(50)