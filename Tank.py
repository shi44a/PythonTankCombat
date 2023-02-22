from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer, QRect, QSize, pyqtSignal, QPoint, QMetaObject, QPropertyAnimation
from PyQt5.QtGui import QPainter, QColor, QPixmap
import time
import Bullet as b


class Tank(QWidget):
    aboutToTankMove = pyqtSignal(QPoint)
    aboutToCreatBullet = pyqtSignal(QPoint)
    aboutToTankExploded = pyqtSignal(QPoint)

    def __init__(self, parent, ):
        super().__init__(parent)
        self.bullet = None
        self.setFixedSize(32, 32)
        self.speed = 4
        self.pixmaplist = ['./img/u1', './img/u2', './img/l1', './img/l2', './img/d1', './img/d2', './img/r1',
                           './img/r2']

        self.direction = 'u'

        self.pixTimer2 = QTimer(self)
        self.pixTimer2.timeout.connect(self.update)
        self.pixTimer2.start(250)
        self.pixChange = 0  # 换坦克动画

        self.aboutToCreatBullet.connect(self.createBullet)
        self.aboutToTankMove.connect(lambda point: self.parentWidget().onTankMove(point))

        self.isHited = False
        self.isMoveing=False

        self.setFocusPolicy(Qt.NoFocus)


    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.save()

        self.changePix(painter)

    def changePix(self, painter):
        if self.isHited is True:
            return

        painter.save()

        if self.direction == 'u':
            if self.pixChange == 0:
                pix = QPixmap(self.pixmaplist[0])
            else:
                pix = QPixmap(self.pixmaplist[1])
        elif self.direction == 'l':
            if self.pixChange == 0:
                pix = QPixmap(self.pixmaplist[2])
            else:
                pix = QPixmap(self.pixmaplist[3])
        elif self.direction == 'd':
            if self.pixChange == 0:
                pix = QPixmap(self.pixmaplist[4])
            else:
                pix = QPixmap(self.pixmaplist[5])
        elif self.direction == 'r':
            if self.pixChange == 0:
                pix = QPixmap(self.pixmaplist[6])
            else:
                pix = QPixmap(self.pixmaplist[7])
        painter.drawPixmap(0, 0, 32, 32, pix.scaled(32, 32, Qt.KeepAspectRatio))
        self.pixChange += 1
        if self.pixChange == 2:
            self.pixChange = 0

    def tankMove(self):
        if self.direction == 'u':
            self.aboutToTankMove.emit(QPoint(self.x(), self.y() - self.speed))
        elif self.direction == 'd':
            self.aboutToTankMove.emit(QPoint(self.x(), self.y() + self.speed))
        elif self.direction == 'l':
            self.aboutToTankMove.emit(QPoint(self.x() - self.speed, self.y()))
        elif self.direction == 'r':
            self.aboutToTankMove.emit(QPoint(self.x() + self.speed, self.y()))

    def tankFire(self):
        if self.isMoveing is False:
            if self.direction == 'u':
                bulletx = int(self.x() + 0.5 * self.width() - 2)
                bullety = self.y()
            elif self.direction == 'l':
                bulletx = self.x()
                bullety = int(self.y() + 0.5 * self.height() - 2)
            elif self.direction == 'd':
                bulletx = int(self.x() + 0.5 * self.width() - 2)
                bullety = self.y() + self.height()
            elif self.direction == 'r':
                bulletx = self.x() + self.width()
                bullety = int(self.y() + 0.5 * self.height() - 2)
        else:
            if self.direction == 'u':
                bulletx = int(self.x() + 0.5 * self.width() - 2)
                bullety = self.y()-4
            elif self.direction == 'l':
                bulletx = self.x()-4
                bullety = int(self.y() + 0.5 * self.height() - 2)
            elif self.direction == 'd':
                bulletx = int(self.x() + 0.5 * self.width() - 2)
                bullety = self.y() + self.height()+4
            elif self.direction == 'r':
                bulletx = self.x() + self.width()+4
                bullety = int(self.y() + 0.5 * self.height() - 2)
        self.aboutToCreatBullet.emit(QPoint(bulletx, bullety))

    def createBullet(self, point):
        if self.bullet is None:
            self.bullet = b.Bullet(self.parentWidget(), self.direction, point)
            self.bullet.destroyed.connect(self.bulletDestroyed)

    def bulletDestroyed(self):
        self.bullet = None

    def tankExploded(self):
        self.isHited = True
        lblExploded = QLabel(self)
        lblExploded.resize(self.size())
        lblExploded.show()
        lblExploded.setStyleSheet("border-image: url(./img/boom)")

        anilblExploded = QPropertyAnimation(lblExploded, b'geometry', self)
        anilblExploded.setDuration(500)
        anilblExploded.setStartValue(QRect(16, 16, 0, 0))
        anilblExploded.setEndValue(QRect(0, 0, 32, 32))
        anilblExploded.finished.connect(lambda: self.deleteLater())
        anilblExploded.start()

    def getTankDirection(self):
        return self.direction

    def getTankSpeed(self):
        return self.speed

