#-*-coding:utf-8-*-

from PyQt5.QtWidgets import *
from PyQt5 import uic
import re

form_fileWindow = uic.loadUiType("UI/fileWindow.ui")[0]
class FileWindow(QDialog, QWidget, form_fileWindow):
    def __init__(self, contents):
        super(FileWindow, self).__init__()
        self.file_contents = contents
        
        self.InitUI()
        self.show()
    
    def InitUI(self):
        self.setupUi(self)
        
        self.textBrw.setPlainText(self.file_contents)
        self.searchButton.clicked.connect(self.search_file_contents)
        
    def search_file_contents(self):
        keyword = self.searchLine.text()
        if keyword:
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            matched_text = ""
            lines = self.file_contents.split('\n')
            for line in lines:
                if pattern.search(line):
                    matched_text += line + '\n' + '\n'
            self.textBrw.setPlainText(matched_text)
            
        elif keyword == "":
            self.textBrw.setPlainText(self.file_contents)
            