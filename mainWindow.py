#-*-coding:utf-8-*-

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

from collectWindow import CollectWindow


form_class = uic.loadUiType("UI/mainWindow.ui")[0]

class MainWindow(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        
        self.pic_name = ''
        self.subj_name = ''
        self.time2str = ''
        
        if not self.is_admin():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("이 프로그램은 관리자(root) 권한으로 실행해야 합니다!")
            msg.setWindowTitle("권한 오류")
            msg.exec_()
            sys.exit()
        
        self.setupUi(self)
        
        #set current time
        self.currentDateTime = QDateTime.currentDateTime()
        self.dateTimeEdit.setDateTime(self.currentDateTime)
        
        self.okButton.clicked.connect(self.setTextFunction)
        self.okButton.clicked.connect(self.collectFunction)
        
        self.cancelButton.clicked.connect(self.closeWindow)

    def is_admin(self):
        try:
            return os.getuid() == 0
        except AttributeError:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
    
        
    def closeWindow(self):
        self.close()   
         
    def collectFunction(self):
        self.hide()
        self.collect = CollectWindow()
        self.collect.exec()
        self.show()
        
    def setTextFunction(self):
        self.pic_name = self.pic_lineEdit.text()
        self.subj_name = self.subj_lineEdit.text()
        time = self.dateTimeEdit.dateTime()
        self.time2str = time.toString(Qt.DefaultLocaleLongDate)
        
if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    mainWindow = MainWindow() 
    
    mainWindow.show()
    app.exec_()