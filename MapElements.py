from PyQt5.QtWidgets import QWidget,QLabel
from PyQt5.QtCore import Qt,QPropertyAnimation,QRect,pyqtSignal
from PyQt5.QtGui import QPainter, QPixmap

class Diamand(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(16, 16)

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.save()

        pix = QPixmap('./img/diamand')
        painter.drawPixmap(0, 0, 16, 16, pix.scaled(16, 16, Qt.KeepAspectRatio))


class Brick(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(16, 16)

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.save()

        pix = QPixmap('./img/brick')
        painter.drawPixmap(0, 0, 16, 16, pix.scaled(16, 16, Qt.KeepAspectRatio))


class River(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(16, 16)

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.save()

        pix = QPixmap('./img/river')
        painter.drawPixmap(0, 0, 16, 16, pix.scaled(16, 16, Qt.KeepAspectRatio))


class Grass(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(16, 16)

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.save()

        pix = QPixmap('./img/grass')
        painter.drawPixmap(0, 0, 16, 16, pix.scaled(16, 16, Qt.KeepAspectRatio))


class Base(QWidget):
    aboutToBaseExploded = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(32, 32)
        self.hp=2
        self.isHited = False

        self.aboutToBaseExploded.connect(lambda: self.parentWidget().gameOver())

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.save()

        self.changePix(painter)

    def changePix(self, painter):
        if self.isHited is True:
            return
        painter.save()
        if self.hp == 2:
            pix = QPixmap('./img/base')
        elif self.hp==1:
            pix = QPixmap('./img/hitbase')
        painter.drawPixmap(0, 0, 32, 32, pix.scaled(32, 32, Qt.KeepAspectRatio))


    def baseHited(self):
        self.hp=self.hp-1
        if self.hp==1:
            self.update()
        elif self.hp==0:
            self.baseExploded()

    def baseExploded(self):
        self.isHited = True

        lblExploded = QLabel(self)
        lblExploded.resize(self.size())
        lblExploded.show()
        lblExploded.setStyleSheet("border-image: url(./img/boom)")

        anilblExploded = QPropertyAnimation(lblExploded, b'geometry', self)
        anilblExploded.setDuration(500)
        anilblExploded.setStartValue(QRect(16, 16, 0, 0))
        anilblExploded.setEndValue(QRect(0, 0, 32, 32))
        anilblExploded.finished.connect(self.explodFinished)
        anilblExploded.start()


    def explodFinished(self):
        self.deleteLater()
        self.aboutToBaseExploded.emit()