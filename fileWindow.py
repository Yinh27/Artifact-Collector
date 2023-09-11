# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5 import uic
import re

form_fileWindow = uic.loadUiType("UI/fileWindow.ui")[0]

class FileWindow(QDialog, QWidget, form_fileWindow):
    def __init__(self, contents):
        super(FileWindow, self).__init__()
        self.file_contents = contents
        self.lines = self.file_contents.split('\n')
        
        if len(self.lines) % 20 == 0:
            self.total_page = len(self.lines) // 20
        else:
            self.total_page = len(self.lines) // 20 + 1
            
        self.current_page = 1
        
        self.InitUI()
        self.show()

    def InitUI(self):
        self.setupUi(self)
        
        self.pagecntLabel.setText(f"{self.current_page} of {self.total_page}")
        self.srt_line = 0
        self.fin_line = 20
        
        self.textBrw.setPlainText('\n'.join(self.lines[self.srt_line:self.fin_line]))
        self.searchButton.clicked.connect(self.search_file_contents)
        self.prevButton.clicked.connect(self.prev_text)
        self.nextButton.clicked.connect(self.next_text)
        
    def next_text(self):
        if not (self.fin_line + 20) > len(self.lines):
            self.current_page += 1
            self.srt_line += 20
            self.fin_line += 20
            self.textBrw.setPlainText('\n'.join(self.lines[self.srt_line:self.fin_line]))
            self.pagecntLabel.setText(f"{self.current_page} of {self.total_page}")
        elif (self.srt_line + 20) > len(self.lines):
            self.current_page += 1
            self.srt_line += 20
            self.textBrw.setPlainText('\n'.join(self.lines[self.srt_line:]))
            self.pagecntLabel.setText(f"{self.current_page} of {self.total_page}")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("[!] End of File")
            msg.setWindowTitle("Alert")
            msg.exec_()
            
    def prev_text(self):
        if not (self.srt_line - 20) < 0:
            self.current_page -= 1
            self.srt_line -= 20
            self.fin_line -= 20
            self.textBrw.setPlainText(str(self.lines[self.srt_line:self.fin_line]))
            self.pagecntLabel.setText(f"{self.current_page} of {self.total_page}")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("[!] Beginning of File")
            msg.setWindowTitle("Alert")
            msg.exec_()

    def search_file_contents(self):
        keyword = self.searchLine.text()
        if keyword:
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            matched_text = ""
            
            for line in self.lines:
                if pattern.search(line):

                    line = pattern.sub(r'<span style="background-color: yellow;">\g<0></span>', line)
                    matched_text += line + '\n'
            
            self.textBrw.setHtml(matched_text)
        else:
            self.textBrw.setPlainText(self.file_contents)
