from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt,pyqtSignal
import menuUI
import pauseUI


class menu(QWidget):
    aboutToGameStart = pyqtSignal(int)

    def __init__(self,parent, ):
        super().__init__(parent)
        self.setStyleSheet('background-color:black;')
        self.ui = menuUI.Ui_Form()
        self.ui.setupUi(self)
        self.ui.lbltc.setStyleSheet('color:rgb(210,105,30)')
        self.ui.lbl1p.setStyleSheet('color:rgb(255,165,0)')
        self.ui.lbl2p.setStyleSheet('color:rgb(105,105,105)')

        self.playerNum=1

        self.grabKeyboard()

    def keyPressEvent(self, QKeyEvent):
        if not QKeyEvent.isAutoRepeat():
            if QKeyEvent.key() == Qt.Key_Space:
                if self.playerNum == 1:
                    self.playerNum = 2
                    self.ui.lbl1p.setStyleSheet("color:rgb(105,105,105)")
                    self.ui.lbl2p.setStyleSheet("color:rgb(255,165,0)")
                else:
                    self.playerNum = 1
                    self.ui.lbl1p.setStyleSheet("color:rgb(255,165,0)")
                    self.ui.lbl2p.setStyleSheet("color:rgb(105,105,105)")
            elif QKeyEvent.key() == Qt.Key_Return:
                self.hide()
                self.aboutToGameStart.emit(self.playerNum)

class pauseMenu(QWidget):
    aboutToGamePause = pyqtSignal(int)

    def __init__(self,parent,):
        super().__init__(parent)
        self.setStyleSheet('background-color:black;')
        self.ui = pauseUI.Ui_Form()
        self.ui.setupUi(self)

        self.ui.lblresume.setStyleSheet('color:rgb(255,165,0)')
        self.ui.lblquit.setStyleSheet('color:rgb(105,105,105)')
        self.ui.lblnew.setStyleSheet('color:rgb(105,105,105)')

        self.option=1

        self.setFocusPolicy(Qt.NoFocus)
