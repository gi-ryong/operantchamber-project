import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_secondwindow = uic.loadUiType("secondwindow.ui")[0] #두 번째창 ui
class secondwindow(QDialog, QWidget,form_secondwindow):
    def __init__(self, parent=None):
        super(secondwindow,self).__init__()
        self.initUI()
        self.show() # 두번째창 실행

    def initUI(self):
        self.setupUi(self)
        self.home.clicked.connect(self.Home)
        
    def Home(self):
        self.close() #창 닫기