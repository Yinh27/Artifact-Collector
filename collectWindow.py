#-*-coding:utf-8-*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
import os
import subprocess
import A_scripts

form_collectWindow = uic.loadUiType("UI/collectWindow.ui")[0]
class CollectWindow(QDialog, QWidget,form_collectWindow):
    def __init__(self):
        super(CollectWindow, self).__init__()
        self.initUI()
        self.show()
        
        self.okButton.clicked.connect(self.collect_and_run)
        self.memdumpCheck.stateChanged.connect(self.update_volatility_check)
        
    def update_volatility_check(self, state):
        if state == Qt.Checked:
            self.volCheck.setEnabled(True)
        else:
            self.volCheck.setEnabled(False)
            self.volCheck.setChecked(False)
            
    def initUI(self):
        self.setupUi(self)
        self.homeButton.clicked.connect(self.home)
    
    def home(self):
        self.close()    
        
    def collect_and_run(self):
        selected_scripts = []
        selected_scripts.append("copy_path")
        
        checkbox_map = {
        self.memdumpCheck: "memory_dump",
        self.volCheck: "volatility_analysis",
        self.pfCheck: "prefetch",
        self.ntfsCheck: "ntfs",
        self.sysinfoCheck: "system_information",
        self.regCheck: "registry_hives",
        self.evtCheck: "event_viewer_logs",
        self.srumCheck: "srum_hosts_services",
        self.envCheck: "environment_variables",
        self.patchCheck: "patch_list",
        self.rprocCheck: "running_process_list",
        self.conninfoCheck: "connection_information",
        self.ipconfigCheck: "ip_config_information",
        self.arpCheck: "arp_information",
        self.netbiosCheck: "netbios_information",
        self.openfpCheck: "open_files_process_information",
        self.schtaskCheck: "scheduled_task_information",
        self.syslogonCheck: "system_login_information",
        self.servCheck: "services_information",
        self.lastactCheck: "last_activity_information",
        self.usrassistCheck: "user_assist_information",
        self.autorunCheck: "autorun_information",
        self.usrregCheck: "user_registry",
        self.brwhistCheck: "browser_history",
        self.recycleCheck: "recycle.bin",
        self.pwshCheck: "powershell_logs",
        self.lnkfCheck: "recent_lnk",
        self.wmiCheck: "wmi_database",
        self.pcaCheck: "pca",
        self.xmlCheck: "windows_task_xml_files",
        self.bmcCheck: "bmc"
        }
        #check scripts
        acq_flag = False
        
        if self.allCheck.isChecked():
            acq_flag = True
            for script_name in checkbox_map.values():
                selected_scripts.append(script_name)
        else:
            for checkbox, script_name in checkbox_map.items():
                if checkbox.isChecked():
                    acq_flag = True
                    # 'CP949' codec error correction
                    if script_name == "volatility_analysis":
                        os.environ['PYTHONIOENCODING'] = 'UTF-8'
                    selected_scripts.append(script_name)
                
        selected_scripts.append("hash")
        
        combined_content = "\n".join("\n".join(A_scripts.acq_scripts[script]) for script in selected_scripts)
        with open("Test.ACQ", "w") as output_file:
            output_file.write(combined_content)
            
        #run bmc-tools
        # if self.bmcCheck.isChecked():
        #     user_home_directory = os.path.expanduser("~")
            
        #     src_path = user_home_directory + "\\AppData\\Local\\Microsoft\\Terminal Server Client\\Cache"
        #     bmc_cmd = ["python", "bmc-tools/bmc-tools.py", "-s", src_path, "-d", "BMC_Results"]
        #     subprocess.run(bmc_cmd, shell=True)
        
        if acq_flag == True:    
            command = ["AchoirX.exe", "/INI:Test.ACQ"]
            subprocess.run(command, shell=True)
            
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("작업이 완료되었습니다!")
        msg.setWindowTitle("완료")
        msg.exec_()