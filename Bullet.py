from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter, QColor


class Bullet(QWidget):
    aboutToBulletMove = pyqtSignal(QPoint)

    def __init__(self, parent, direction, pos):
        super().__init__(parent)
        self.setFixedSize(4, 4)
        self.speed = 1
        self.direction = direction

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.bulletMove)
        self.timer.start(10)

        self.show()
        self.move(pos)

        self.aboutToBulletMove.connect(lambda point: self.parentWidget().onBulletMove(point))

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.save()
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(0, 0, 4, 4)

    def bulletMove(self):
        if self.direction == 'u':
            x = self.x()
            y = self.y() - self.speed
        elif self.direction == 'l':
            x = self.x() - self.speed
            y = self.y()
        elif self.direction == 'd':
            x = self.x()
            y = self.y() + self.speed
        elif self.direction == 'r':
            x = self.x() + self.speed
            y = self.y()
        self.aboutToBulletMove.emit((QPoint(x, y)))

    def getBulletDirection(self):
        return self.direction

    def getBulletSpeed(self):
        return self.speed
