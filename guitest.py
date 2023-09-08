import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QCheckBox, QMessageBox
from PyQt5.QtCore import Qt
import A_scripts
import subprocess

class ScriptCollector(QWidget):
    def __init__(self):
        super().__init__()
        
        # 관리자 권한 확인
        if not self.is_admin():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("이 프로그램은 관리자(root) 권한으로 실행해야 합니다!")
            msg.setWindowTitle("권한 오류")
            msg.exec_()
            sys.exit()
        
        self.init_ui()

    def is_admin(self):
        # 현재 프로세스가 관리자(root) 권한으로 실행되었는지 확인 (Windowds, Linux)
        try:
            return os.getuid() == 0
        except AttributeError:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0

    def init_ui(self):
        layout = QVBoxLayout()

        self.memorydump_check = QCheckBox('Memory_Dump', self)
        self.volatility_analysis_check = QCheckBox('Volatility_analysis', self)
        
        # 기본적으로 volatility_analysis_check를 비활성화합니다.
        self.volatility_analysis_check.setEnabled(False)

        # memorydump_check의 상태가 변경되면 update_volatility_check 메서드를 호출합니다.
        self.memorydump_check.stateChanged.connect(self.update_volatility_check)

        self.prefetch_check = QCheckBox('Prefetch', self)
        self.ntfs_check = QCheckBox('NTFS', self)
        self.sysinfo_check = QCheckBox('System Information', self)
        self.reg_check = QCheckBox('Registry Hives', self)
        self.evt_check = QCheckBox('EventViewer Logs', self)
        self.srum_check = QCheckBox('SRUM, Hosts, Services', self)
        self.env_check = QCheckBox('Environment Variables', self)
        self.patch_check = QCheckBox('Patch List', self)
        self.rproc_check = QCheckBox('Running Process List Information', self)
        self.conninfo_check = QCheckBox('Connection Information', self)
        self.ipconfig_check = QCheckBox('IP Config Information', self)
        self.arp_check = QCheckBox('ARP Information', self)
        self.netbios_check = QCheckBox('NetBIOS Information', self)
        self.openfp_check = QCheckBox('Open Files/Process Information', self)
        self.schtask_check = QCheckBox('Scheduled Task Information', self)
        self.syslogon_check = QCheckBox('System Logon Information', self)
        self.serv_check = QCheckBox('Services Information', self)
        self.lastact_check = QCheckBox('Last Activity Information', self)
        self.userassist_check = QCheckBox('User Assist Information', self)
        self.autorun_check = QCheckBox('AutoRun Information', self)
        self.userreg_check = QCheckBox('Current/All User Registry', self)
        self.browhist_check = QCheckBox('Browser History', self)
        self.recycle_check = QCheckBox('$Recycle.Bin', self)
        self.pwsh_check = QCheckBox('PowerShell Logs', self)
        self.lnkf_check = QCheckBox('Recent LNK Files', self)
        self.wmi_check = QCheckBox('WMI CIM database files', self)
        self.pca_check = QCheckBox('Program Compatibility Assistant files(Windows 11)', self)
        self.wtask_check = QCheckBox('Windows Task XML Files', self)

        collect_btn = QPushButton('수집', self)
        collect_btn.clicked.connect(self.collect_and_run)

        layout.addWidget(self.memorydump_check)
        layout.addWidget(self.volatility_analysis_check)
        layout.addWidget(self.prefetch_check)
        layout.addWidget(self.ntfs_check)
        layout.addWidget(self.sysinfo_check)
        layout.addWidget(self.reg_check)
        layout.addWidget(self.evt_check)
        layout.addWidget(self.srum_check)
        layout.addWidget(self.env_check)
        layout.addWidget(self.patch_check)
        layout.addWidget(self.rproc_check)
        layout.addWidget(self.conninfo_check)
        layout.addWidget(self.ipconfig_check)
        layout.addWidget(self.arp_check)
        layout.addWidget(self.netbios_check)
        layout.addWidget(self.openfp_check)
        layout.addWidget(self.schtask_check)
        layout.addWidget(self.syslogon_check)
        layout.addWidget(self.serv_check)
        layout.addWidget(self.lastact_check)
        layout.addWidget(self.userassist_check)
        layout.addWidget(self.autorun_check)
        layout.addWidget(self.userreg_check)
        layout.addWidget(self.browhist_check)
        layout.addWidget(self.recycle_check)
        layout.addWidget(self.pwsh_check)
        layout.addWidget(self.lnkf_check)
        layout.addWidget(self.wmi_check)
        layout.addWidget(self.pca_check)
        layout.addWidget(self.wtask_check)
        layout.addWidget(collect_btn)

        self.setLayout(layout)
        self.setWindowTitle('ACQ Script Collector')
        self.show()

    def update_volatility_check(self, state):
        """memorydump_check의 상태에 따라 volatility_analysis_check를 활성화/비활성화합니다."""
        if state == Qt.Checked:
            self.volatility_analysis_check.setEnabled(True)
        else:
            self.volatility_analysis_check.setEnabled(False)
            self.volatility_analysis_check.setChecked(False)  # 필요한 경우 체크를 해제합니다.

    def collect_and_run(self):
        selected_scripts = []
        selected_scripts.append("copy_path")

        if self.memorydump_check.isChecked():
            selected_scripts.append("memory_dump")
        if self.volatility_analysis_check.isChecked():
            selected_scripts.append("volatility_analysis")
            # 환경변수 설정
            os.environ['PYTHONIOENCODING'] = 'UTF-8'
        if self.prefetch_check.isChecked():
            selected_scripts.append("prefetch")
        if self.ntfs_check.isChecked():
            selected_scripts.append("ntfs")
        if self.sysinfo_check.isChecked():
            selected_scripts.append("system_information")
        if self.reg_check.isChecked():
            selected_scripts.append("registry_hives")
        if self.evt_check.isChecked():
            selected_scripts.append("event_viewer_logs")
        if self.srum_check.isChecked():
            selected_scripts.append("srum_hosts_services")
        if self.env_check.isChecked():
            selected_scripts.append("environment_variables")
        if self.patch_check.isChecked():
            selected_scripts.append("patch_list")
        if self.rproc_check.isChecked():
            selected_scripts.append("running_process_list")
        if self.conninfo_check.isChecked():
            selected_scripts.append("connection_information")
        if self.ipconfig_check.isChecked():
            selected_scripts.append("ip_config_information")
        if self.arp_check.isChecked():
            selected_scripts.append("arp_information")
        if self.netbios_check.isChecked():
            selected_scripts.append("netbios_information")
        if self.openfp_check.isChecked():
            selected_scripts.append("open_files_process_information")
        if self.schtask_check.isChecked():
            selected_scripts.append("scheduled_task_information")
        if self.syslogon_check.isChecked():
            selected_scripts.append("system_login_information")
        if self.serv_check.isChecked():
            selected_scripts.append("services_information")
        if self.lastact_check.isChecked():
            selected_scripts.append("last_activity_information")
        if self.userassist_check.isChecked():
            selected_scripts.append("user_assist_information")
        if self.autorun_check.isChecked():
            selected_scripts.append("autorun_information")
        if self.userreg_check.isChecked():
            selected_scripts.append("user_registry")
        if self.browhist_check.isChecked():
            selected_scripts.append("browser_history")
        if self.recycle_check.isChecked():
            selected_scripts.append("recycle.bin")
        if self.pwsh_check.isChecked():
            selected_scripts.append("powershell_logs")
        if self.lnkf_check.isChecked():
            selected_scripts.append("recent_lnk")
        if self.wmi_check.isChecked():
            selected_scripts.append("wmi_database")
        if self.pca_check.isChecked():
            selected_scripts.append("pca")
        if self.wtask_check.isChecked():
            selected_scripts.append("windows_task_xml_files")
        
        selected_scripts.append("hash")

        combined_content = "\n".join("\n".join(A_scripts.acq_scripts[script]) for script in selected_scripts)
        with open("Test.ACQ", "w") as output_file:
            output_file.write(combined_content)

		# Windows용 코드라서 다른 운영체제도 될 지는 모름
        command = ["AchoirX.exe", "/INI:Test.ACQ"]
        subprocess.run(command, shell=True)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("작업이 완료되었습니다!")
        msg.setWindowTitle("완료")
        msg.exec_()

app = QApplication(sys.argv)
window = ScriptCollector()
sys.exit(app.exec_())