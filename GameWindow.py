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
import gc


class gameWindow(QWidget):
    aboutToGameOver = pyqtSignal()
    aboutToClose = pyqtSignal()

    def __init__(self,playernum,parent=None):
        super().__init__()
        self.setFixedSize(640, 480)
        self.setStyleSheet('background-color:black;')
        self.playernum=playernum

        self.createMap(m.maplist)
        self.createPlayer()

        self.etank={}
        self.etankNum=20
        self.createETank()
        self.createETank()

        # self.mainTimer = QTimer(self)
        # self.mainTimer.timeout.connect(self.createETank)
        # self.mainTimer.start(10)

        self.createETankTimer=QTimer(self)
        self.createETankTimer.timeout.connect(self.createETank)
        self.createETankTimer.start(15000)

        self.grabKeyboard()
        self.setFocusPolicy(Qt.StrongFocus)

        self.gamePause=None


    def createMap(self, maplist):
        for i in range(len(maplist)):
            row = maplist[i]
            for j in range(len(row)):
                x = 16 * j
                y = 16 * i
                char = row[j]
                if char == 'D':
                    self.d = MapE.Diamand(self)
                    self.d.move(x, y)
                elif char == 'B':
                    self.b = MapE.Brick(self)
                    self.b.move(x, y)
                elif char == 'R':
                    self.r = MapE.River(self)
                    self.r.move(x, y)
                elif char == 'G':
                    self.g = MapE.Grass(self)
                    self.g.move(x, y)
                elif char == 'b':
                    self.base = MapE.Base(self)
                    self.base.move(x, y)

    def createPlayer(self):
        self.ft = ft.FTank(self)
        self.ft.move(256, 448)
        self.ft.lower()
        self.st=None
        if self.playernum == 2:
            self.newPlayer()

    def newPlayer(self):
        self.st = st.STank(self)
        self.st.move(384, 448)
        self.st.show()
        self.st.lower()
        self.playernum=2

    def createETank(self):
        if self.etankNum==0:
            self.createETankTimer.stop()
        else:
            etankPos = self.etankPos()
            while etankPos is None:
                etankPos = self.etankPos()
            x=etankPos.x()
            y=etankPos.y()
            self.etank[self.etankNum]=et.ETank(self)
            self.etank[self.etankNum].setGeometry(x, y, 32, 32)
            self.etank[self.etankNum].show()
            self.etankNum =self.etankNum-1

    def etankPos(self):
        etankx=random.randrange(0,609,32)
        etanky=0
        widget1=self.childAt(etankx, etanky)
        widget2 = self.childAt(etankx, etanky+16)
        widget3 = self.childAt(etankx+16, etanky)
        widget4 = self.childAt(etankx+16, etanky+16)
        if (widget1 is None) and (widget2 is None)  and (widget3 is None)  and (widget4 is None):
            etankPos=QPoint(etankx,etanky)
            return etankPos

    def gameOver(self):
        gameOver = QLabel('GAME OVER',self)
        gameOver.setGeometry(0, 140, 640, 200)
        gameOver.setStyleSheet('font-size:80px;font-weight:bold;color:rgb(0,0,205);background:rgb(0,0,0,0)')
        gameOver.setAlignment(Qt.AlignHCenter)
        gameOver.show()

        anigameOver = QPropertyAnimation(gameOver, b'pos', self)
        anigameOver.setDuration(2000)
        anigameOver.setStartValue(QPoint(0, 480))
        anigameOver.setEndValue(QPoint(0, 140))
        anigameOver.start()

    def gamePauseOptionMenu(self):
        self.gamePause=menu.pauseMenu(self)
        self.gamePause.setGeometry(170, 90, 400, 300)
        self.gamePause.show()
        self.gamePause.aboutToGamePause.connect(lambda option:self.pauseOption(option))

    def pauseOption(self,option):
        if option==1:
            self.resume(True)
        elif option==2:
            self.close()
            self.aboutToClose.emit()
        elif option==3:
            self.newPlayer()
            self.resume(True)


    def keyPressEvent(self, QKeyEvent):
        if not QKeyEvent.isAutoRepeat():
            if QKeyEvent.key() == Qt.Key_Escape:
                self.gamePauseOptionMenu()
                self.resume(False)
            if self.ft is not None:
                if QKeyEvent.key() == Qt.Key_Up:
                    self.ft.direction = 'u'
                    self.ft.isPressed = True
                    self.ft.isMoveing = True
                elif QKeyEvent.key() == Qt.Key_Down:
                    self.ft.direction = 'd'
                    self.ft.isPressed = True
                    self.ft.isMoveing = True
                elif QKeyEvent.key() == Qt.Key_Left:
                    self.ft.direction = 'l'
                    self.ft.isPressed = True
                    self.ft.isMoveing = True
                elif QKeyEvent.key() == Qt.Key_Right:
                    self.ft.direction = 'r'
                    self.ft.isPressed = True
                    self.ft.isMoveing = True
                elif QKeyEvent.key() == Qt.Key_0:
                    self.ft.tankFire()
            if self.st is not None:
                if QKeyEvent.key() == Qt.Key_W:
                    self.st.direction = 'u'
                    self.st.isPressed = True
                    self.st.isMoveing = True
                elif QKeyEvent.key() == Qt.Key_S:
                    self.st.direction = 'd'
                    self.st.isPressed = True
                    self.st.isMoveing = True
                elif QKeyEvent.key() == Qt.Key_A:
                    self.st.direction = 'l'
                    self.st.isPressed = True
                    self.st.isMoveing = True
                elif QKeyEvent.key() == Qt.Key_D:
                    self.st.direction = 'r'
                    self.st.isPressed = True
                    self.st.isMoveing = True
                elif QKeyEvent.key() == Qt.Key_F:
                    self.st.tankFire()
            if self.gamePause is not None:
                if QKeyEvent.key() == Qt.Key_Space:
                    if self.playernum == 1:
                        if self.gamePause.option == 1:
                            self.gamePause.option = 2
                            self.gamePause.ui.lblresume.setStyleSheet('color:rgb(105,105,105)')
                            self.gamePause.ui.lblquit.setStyleSheet('color:rgb(255,165,0)')
                            self.gamePause.ui.lblnew.setStyleSheet('color:rgb(105,105,105)')
                        elif self.gamePause.option == 2:
                            self.gamePause.option = 3
                            self.gamePause.ui.lblresume.setStyleSheet('color:rgb(105,105,105)')
                            self.gamePause.ui.lblquit.setStyleSheet('color:rgb(105,105,105)')
                            self.gamePause.ui.lblnew.setStyleSheet('color:rgb(255,165,0)')
                        elif self.gamePause.option == 3:
                            self.gamePause.option = 1
                            self.gamePause.ui.lblresume.setStyleSheet('color:rgb(255,165,0)')
                            self.gamePause.ui.lblquit.setStyleSheet('color:rgb(105,105,105)')
                            self.gamePause.ui.lblnew.setStyleSheet('color:rgb(105,105,105)')
                    elif self.playernum == 2:
                        if self.gamePause.option == 1:
                            self.gamePause.option = 2
                            self.gamePause.ui.lblresume.setStyleSheet('color:rgb(105,105,105)')
                            self.gamePause.ui.lblquit.setStyleSheet('color:rgb(255,165,0)')
                        elif self.gamePause.option == 2:
                            self.gamePause.option = 1
                            self.gamePause.ui.lblresume.setStyleSheet('color:rgb(255,165,0)')
                            self.gamePause.ui.lblquit.setStyleSheet('color:rgb(105,105,105)')
                elif QKeyEvent.key() == Qt.Key_Return:
                    self.gamePause.hide()
                    self.gamePause.aboutToGamePause.emit(self.gamePause.option)

    def keyReleaseEvent(self, QKeyEvent):
        if not QKeyEvent.isAutoRepeat():
            if not QKeyEvent.isAutoRepeat():
                if QKeyEvent.key() == Qt.Key_Up or QKeyEvent.key() == Qt.Key_Down or QKeyEvent.key() == Qt.Key_Left or QKeyEvent.key() == Qt.Key_Right:
                    self.ft.isPressed = False
                    self.ft.isMoveing = False
                    QKeyEvent.accept()
            if self.st is not None:
                if QKeyEvent.key() == Qt.Key_W or QKeyEvent.key() == Qt.Key_S or QKeyEvent.key() == Qt.Key_A or QKeyEvent.key() == Qt.Key_D:
                    self.st.isPressed = False
                    self.st.isMoveing = False
                    QKeyEvent.accept()

    def resume(self,bool):
        pass
        # if bool== False:
        #     print('暂停')
        #     self.createETankTimer.stop()
        #     self.ft.moveTimer.stop()
        #     if self.st is not None:
        #         self.st.moveTimer.stop()
        #     for var in globals().values():
        #         if type(var) is et.ETank:
        #             var.actionTimer.stop()
        #             var.moveTimer.stop()
        #             var.fireTimer.stop()
        #         elif type(var) is b.Bullet:
        #             var.timer.stop()
        # else:
        #     print('开始')
        #     self.createETankTimer.start(15000)
        #     self.ft.moveTimer.start(50)
        #     if self.st is not None:
        #         self.st.moveTimer.start(50)
        #     for var in globals().values():
        #         if type(var) is et.ETank:
        #             var.actionTimer.start(50)
        #             var.moveTimer.start(400)
        #             var.fireTimer.start(500)
        #         elif type(var) is b.Bullet:
        #             var.timer.start(10)


    def onTankMove(self, point):
        tank = self.sender()
        direction = tank.getTankDirection()
        speed = tank.getTankSpeed()
        x = point.x()
        y = point.y()
        if x < 0 or x > 608 or y < 0 or y > 448:
            pass
        else:
            self.tankCollisionDetection(x, y, direction, speed, 0)

    def tankCollisionDetection(self, x, y, direction, speed, i):
        tank = self.sender()
        if direction == 'u':
            a = 0
            b = 1
            widget1 = self.childAt(x, y)
            widget2 = self.childAt(x + 31, y)
            widget3=self.childAt(x + 16, y)
        elif direction == 'l':
            a = 1
            b = 0
            widget1 = self.childAt(x, y)
            widget2 = self.childAt(x, y + 31)
            widget3 = self.childAt(x , y+ 16)
        elif direction == 'd':
            a = 0
            b = -1
            widget1 = self.childAt(x, y + 31)
            widget2 = self.childAt(x + 31, y + 31)
            widget3 = self.childAt(x+16, y + 31)
        elif direction == 'r':
            a = -1
            b = 0
            widget1 = self.childAt(x + 31, y)
            widget2 = self.childAt(x + 31, y + 31)
            widget3 = self.childAt(x + 31, y + 16)

        if widget1 is None and widget2 is None:
            if widget3 is None:
                tank.move(x, y)
                return
            else:
                cn3 = widget3.metaObject().className()
                if cn3 == 'Diamand' or cn3 == 'River' or cn3 == 'Brick':
                    return
        elif widget1 is not None and widget2 is not None:
            cn1 = widget1.metaObject().className()
            cn2 = widget2.metaObject().className()
            if cn1 == 'Diamand' or cn1 == 'River' or cn1 == 'Brick' or cn1=='Base' or (re.search('Tank', cn1) is not None)\
                    or cn2 == 'Diamand' or cn2 == 'River' or cn2 == 'Brick' or cn2=='Base' or (re.search('Tank', cn2) is not None):
                i = i + 1
                if i <= speed:
                    x = x + a
                    y = y + b
                    self.tankCollisionDetection(x, y, direction, speed, i)
                elif i > speed:
                    return
            else:
                tank.move(x, y)
                return
        elif widget1 is not None and widget2 is None:
            cn1 = widget1.metaObject().className()
            if cn1 == 'Diamand' or cn1 == 'River' or cn1 == 'Brick' or cn1=='Base' or (re.search('Tank', cn1) is not None):
                i = i + 1
                if i <= speed:
                    x = x + a
                    y = y + b
                    self.tankCollisionDetection(x, y, direction, speed, i)
                elif i > speed:
                    return
            else:
                tank.move(x, y)
                return
        elif widget1 is None and widget2 is not None:
            cn2 = widget2.metaObject().className()
            if cn2 == 'Diamand' or cn2 == 'River' or cn2 == 'Brick' or cn2=='Base' or (re.search('Tank', cn2) is not None):
                i = i + 1
                if i <= speed:
                    x = x + a
                    y = y + b
                    self.tankCollisionDetection(x, y, direction, speed, i)
                elif i > speed:
                    return
            else:
                tank.move(x, y)
                return

    def onBulletMove(self, point):
        bullet = self.sender()  # sender()
        direction = bullet.getBulletDirection()
        x = point.x()
        y = point.y()
        if x >= 0 and x <= 636 and y >= 0 and y <= 476:
            self.bulletCollisionDetection(x, y, direction)
        else:
            bullet.deleteLater()

    def bulletCollisionDetection(self, x, y, direction):
        bullet = self.sender()
        if direction == 'u':
            widget1 = self.childAt(x, y)
            widget2 = self.childAt(x + 3, y)
        elif direction == 'l':
            widget1 = self.childAt(x, y)
            widget2 = self.childAt(x, y + 3)
        elif direction == 'd':
            widget1 = self.childAt(x, y + 3)
            widget2 = self.childAt(x + 3, y + 3)
        elif direction == 'r':
            widget1 = self.childAt(x + 3, y)
            widget2 = self.childAt(x + 3, y + 3)

        if widget1 is None and widget2 is None:
            bullet.move(x, y)
            return
        elif widget1 is None and widget2 is not None:
            cn2 = widget2.metaObject().className()
            if cn2 == 'Diamand':
                bullet.deleteLater()
                return
            elif cn2 == 'Bullet':
                bullet.deleteLater()
                return
            elif re.search('Tank', cn2) is not None:
                widget2.tankExploded()
                bullet.deleteLater()
                return
            elif cn2 == 'Brick':
                widget2.deleteLater()
                bullet.deleteLater()
                return
            elif cn2=='Base':
                widget2.baseHited()
                bullet.deleteLater()
                return
            else:
                bullet.move(x, y)
                return
        else:
            cn1 = widget1.metaObject().className()
            if cn1 == 'Diamand':
                bullet.deleteLater()
                return
            elif cn1 == 'Bullet':
                bullet.deleteLater()
                return
            elif (re.search('Tank', cn1) is not None):
                bullet.deleteLater()
                widget1.tankExploded()
                return
            elif cn1 == 'Brick':
                bullet.deleteLater()
                widget1.deleteLater()
                return
            elif cn1=='Base':
                widget1.baseHited()
                bullet.deleteLater()
                return
            else:
                bullet.move(x, y)
                return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = gameWindow()
    w.show()

    sys.exit(app.exec_())
