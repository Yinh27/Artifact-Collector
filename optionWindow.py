from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import *
from PyQt5 import uic
import subprocess
import os
import time
from searchWindow import FileSearchApp

form_optionWindow = uic.loadUiType("UI/optionWindow.ui")[0]
class OptionWindow(QDialog, form_optionWindow):
    def __init__(self, dir):
        super(OptionWindow, self).__init__()
        self.setupUi(self)
        self.show()
        
        self.dir = dir
        
        self.okButton.clicked.connect(self.vol3_run)
        self.cancelButton.clicked.connect(self.go_to_search)
        
        
    def vol3_run(self):
        dump_path = self.dir + r"\MemDump\WinPmemDump.Raw"
        VR0 = "python"
        VR2 = r".\Vol\vol.exe"
        vol_list = [["windows.pslist.PsList", r"\VoLoki\PSList.dat"],
                    ["windows.pstree.PsTree", r"\VoLoki\PSTree.dat"],
                    ["windows.psscan.PsScan", r"\VoLoki\PSScan.dat"],
                    ["windows.modules.Modules", r"\VoLoki\Modules.dat"],
                    ["windows.modscan.ModScan", r"\VoLoki\ModScan.dat"],
                    ["windows.driverscan.DriverScan", r"\VoLoki\DriverScan.dat"],
                    ["windows.getservicesids.GetServiceSIDs", r"\VoLoki\SvcScan.dat"],
                    ["windows.cmdline.CmdLine", r"\VoLoki\CmdLine.dat"],
                    ["windows.netscan.NetScan", r"\VoLoki\Netscan.dat"],
                    ["windows.filescan.FileScan", r"\VoLoki\OpenFiles.dat"],
                    ["windows.pslist.PsList", r"\VoLoki\PSList.csv"]
                    ]
        os.environ['PYTHONIOENCODING'] = 'UTF-8'
        for src, dst in vol_list:
            command = [VR0, VR2, "-f", dump_path, src, ">>", self.dir + dst]
            subprocess.run(command, shell=True)
            time.sleep(1)
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("작업이 완료되었습니다!")
        msg.setWindowTitle("완료")
        msg.exec_()
        
        self.close()
        self.search = FileSearchApp()
    
    def go_to_search(self):
        self.close()
        self.search = FileSearchApp()
        