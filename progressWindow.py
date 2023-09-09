from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import *
from PyQt5 import uic
import subprocess
from searchWindow import FileSearchApp

form_progressWindow = uic.loadUiType("UI/progressWindow.ui")[0]

class CommandRunner(QThread):
    finished = pyqtSignal()
    progress_updated = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        command = ["AchoirX.exe", "/INI:Test.ACQ"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        
        while True:
            try:
                output = process.stdout.readline().decode('utf-8')
            except UnicodeDecodeError:
                pass
            if output == '' and process.poll() is not None:
                break
            
            if "I'm Done!" in output:
                    self.progress_updated.emit(1)
        
        self.finished.emit()

class ProgressWindow(QDialog, form_progressWindow):
    def __init__(self, num):
        super(ProgressWindow, self).__init__()
        self.setupUi(self)
        self.show()
        self.script_length = num
        
        self.command_runner = CommandRunner()
        self.command_runner.finished.connect(self.msg_box)
        self.command_runner.progress_updated.connect(self.update_progress)
        self.command_runner.start()
    
    def msg_box(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("작업이 완료되었습니다!")
        msg.setWindowTitle("완료")
        msg.exec_()
        
        self.hide()
        self.search = FileSearchApp()
        
    def update_progress(self, value):
        current_value = self.progressBar.value()
        self.progressBar.setValue(current_value + value)
