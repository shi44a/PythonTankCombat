import sys
from PyQt5.QtWidgets import QApplication, QWidget,QLabel
from PyQt5.QtCore import Qt, QTimer, QRect, pyqtSignal, QPoint, QMetaObject,QPropertyAnimation
from PyQt5.QtGui import QPainter, QColor, QPixmap
import MapElements as MapE
import Bullet as b
import FTank as ft
import STank as st
import ETank as et
import MapList as m
import menu
import re
import random
import GameWindow as gw

class tankCombat(QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.setFixedSize(640, 480)
        self.setStyleSheet('background-color:black;')
        self.menu = menu.menu(self)
        self.menu.show()
        self.menu.aboutToGameStart.connect(lambda playernum:self.gameStart(playernum))


    def gameStart(self,*playernum):
        self.hide()
        self.gamewindow =gw.gameWindow(*playernum)
        self.gamewindow.setFixedSize(640, 480)
        self.gamewindow.show()
        self.gamewindow.aboutToClose.connect(self.showMenu)



    def showMenu(self):
        self.show()
        self.menu.show()
        self.menu.setFocusPolicy(Qt.StrongFocus)

    # def keyPressEvent(self, QKeyEvent):
    #
    # def keyReleaseEvent(self, QKeyEvent):
    #



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = tankCombat()
    w.show()

    sys.exit(app.exec_())