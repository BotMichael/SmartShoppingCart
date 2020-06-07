import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton

from Edge_Client_RP1 import Edge_Client_RP1

import time


class BYE(QMainWindow):
    def __init__(self):
        super(BYE, self).__init__()
        self.init_ui()
 
    def init_ui(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.resize(450, 600)
        self.setWindowTitle('Bye~')

        self._banner = QtWidgets.QLabel(self)
        self._banner.setGeometry(70, 20, 301, 111)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(48)
        self._banner.setFont(font)
        self._banner.setObjectName("_banner")
        self._banner.show()
        _translate = QtCore.QCoreApplication.translate
        self._banner.setText(_translate("MainWindow", "Bye~"))
        
        self.btn = QPushButton('Return Welcome', self)
        self.btn.setGeometry(20, 170, 400, 200)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(36)
        self.btn.setFont(font)
        self.btn.clicked.connect(self.slot_btn1_function)

        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        
        QtCore.QMetaObject.connectSlotsByName(self)

    def slot_btn1_function(self):
        self.hide()

        rpi1 = Edge_Client_RP1()
        rpi1.quit()
        rpi1.init_session()

        from Main import First_UI
        self.f = First_UI()
        self.f.show()
