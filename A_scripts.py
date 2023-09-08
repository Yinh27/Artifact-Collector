# ACQ 스크립트들 (copy_path, hash는 다른 스크립트 선택 시 무조건 선택돼야 함)
acq_scripts = {
    "copy_path": [
        "SET:CopyPath=Part"
    ],
    "memory_dump": [
        "SAY:  ",
        "VER:Windows",
        "SAY:",
        "SAY:[+] Now Dumping Memory...",
        "SAY:",
        "SAY:  WARNING: This will take while, and will create a HUGE memory image File.",
        "SAY:",
        "N<<:&Dsa &Mem",
        "SAY:[!] Not Enough disk space in &ACQ to Capture Memory: &MEM ...",
        "SAY:[!] Bypassing Memory Capture!",
        "END:",
        "N>>:&Dsa &Mem",
        r"ACQ:\MemDump",
        "64B:",
        r"EXE:\MEM\winpmem_mini_x64_rc2.exe &Acq\WinPmemDump.Raw",
        "END:",
        "32B:",
        r"EXE:\MEM\winpmem_mini_x86_rc2.exe &Acq\WinPmemDump.Raw",
        "END:"
	],
	"volatility_analysis": [
        r"VR2:.\Vol\Volatility3-2.4.1\vol.py",
        "VR0:py &VR2",
        "CKN:&VR2",
        "Say:",
        "Say:[!] Volatility Not Found! Exiting...",
        "Bye:",
        "END:"

        "Say:",
        r"VR1:&Acq\WinPmemDump.Raw",
        r"ACQ:\VoLoki",
        "Say:",
        "Say:[+] Gathering Basic Memory Dump Info...",
        "Say:",
        "Say:[+] Parsing Process List...",
        r"SYS:&VR0 -f &VR1 windows.pslist.PsList --exestdout=&acn\VoLoki\PSList.dat",
        "Say:",
        "Say:[+] Parsing Process Tree...",
        r"SYS:&VR0 -f &VR1 windows.pstree.PsTree --exestdout=&acn\VoLoki\PSTree.dat",
        "Say:",
        "Say:[+] Parsing Complete Process Scan (Unlinked Processes)...",
        r"SYS:&VR0 -f &VR1 windows.psscan.PsScan --exestdout=&acn\VoLoki\PSScan.dat",
        "Say:",
        "Say:[+] Parsing Modules...",
        r"SYS:&VR0 -f &VR1 windows.modules.Modules --exestdout=&acn\VoLoki\Modules.dat",
        "Say:",
        "Say:[+] Parsing Complete Module Scan (Unlinked Modules)...",
        r"SYS:&VR0 -f &VR1 windows.modscan.ModScan --exestdout=&acn\VoLoki\ModScan.dat",
        "Say:",
        "Say:[+] Parsing Complete Driver Scan...",
        r"SYS:&VR0 -f &VR1 windows.driverscan.DriverScan --exestdout=&acn\VoLoki\DriverScan.dat",
        "Say:",
        "Say:[+] Parsing Complete Services Scan...",
        r"SYS:&VR0 -f &VR1 windows.getservicesids.GetServiceSIDs --exestdout=&acn\VoLoki\SvcScan.dat",
        "Say:",
        "Say:[+] Parsing Command Line History...",
        r"SYS:&VR0 -f &VR1 windows.cmdline.CmdLine --exestdout=&acn\VoLoki\CmdLine.dat",
        "Say:",
        "Say:[+] Parsing Network Info...",
        r"SYS:&VR0 -f &VR1 windows.netscan.NetScan --exestdout=&acn\VoLoki\Netscan.dat",
        "Say:",
        "Say:[+] Parsing Open Files Info...",
        r"SYS:&VR0 -f &VR1 windows.filescan.FileScan --exestdout=&acn\VoLoki\OpenFiles.dat",
        "Say:",
        "Say:[+] Creating Process List CSV for Module Processing...",
        r"SYS:&VR0 -r csv -f &VR1 windows.pslist.PsList --exestdout=&acn\VoLoki\PSList.csv",
        "Say:",
        "Bye:",
        "END:"
    ],
    "prefetch": [
        "VER:Windows",
        "SAY:[+] Prefetch - Extracting Prefetch Directory...",
        r"ACQ:\Prfpy",
        r'CPY:"&Win\prefetch\**\*" "&Acq"',
        r"ACQ:\Prfpy\pfcsv",
        r"ACQ:\Prfpy",
        r"FOR:&Acq\*.pf",
        "32B:",
        r'EXE:\SYS\WinPrefetchView.exe /scomma "&Acq\pfcsv\&FNM.csv" /prefetchfile "&FOR"',
        "END:",
        "64B:",
        r'EXE:\SYS\64Bit\WinPrefetchView.exe /scomma "&Acq\pfcsv\&FNM.csv" /prefetchfile "&FOR"',
        "END:"
    ],
    "ntfs": [
        "VER:Windows",
        "SAY:",
        "SAY: [+] NTFS Artifacts - Copy Raw $MFT(s)...",
        "SAY:",
        "DSK:Fixed",
        r"ACQ:\RawData",
        r"EXE:\TSK\sleuthkit-4.10.0-win32\bin\fcat.exe -f ntfs $MFT \\.\&dsk: --exestdout=&acn\RawData\MFT-&Dsk",
        "SAY:",
        "SAY: [+] NTFS Artifacts - Copy Raw $LogFile...",
        "SAY:",
        r"EXE:\TSK\sleuthkit-4.10.0-win32\bin\fcat.exe -f ntfs $LogFile \\.\&dsk: --exestdout=&acn\RawData\LogFile-&Dsk",
        "SAY:",
        "SAY: [+] NTFS Artifacts - Now Extracting USNJrnl...",
        "SAY:",
        r"EXE:\DSK\ExtractUSNJrnl.exe /DevicePath:c: /OutputPath:&Acq",
        "SAY:",
        "SAY: [+] NTFS Artifacts - Now Parsing USNJrnl...",
        "SAY:",
        r"SYS:fsutil usn enumdata 1 0 1 C: --exestdout=&acn\RawData\USNJrnl.dat",
        r"SYS:fsutil usn readjournal C: csv --exestdout=&acn\RawData\USNJrnl.csv",
        "SAY:",
        "SAY: [+] NTFS Artifacts - Now Parsing $MFT...",
        "SAY:",
        r"EXE:\DSK\mftdump.exe &acn\RawData\MFT-&Dsk /o &acn\RawData\parsed_mft-&Dsk.txt",
        "END:"
    ],
    "system_information": [
        "VER:Windows",
        "SAY:",
        "SAY: [+] Gathering System Information...",
        "SAY:",
        "ACQ:\\",
        r"EXE:\SYS\PSInfo.exe /accepteula -s --exestdout=&acn\Info.dat",
        "SAY:",
        "SAY: [+] Gathering System Audit Information...",
        "SAY:",
        r"EXE:\SYS\WinAudit.exe /r=gsoPxuTUeERNtnzDaIbMpmidcSArCOHG /f=&Acq\WinAudit.htm /l=&Acq\WinAudLog.txt",
        "SAY:",
        "SAY: [+] Gathering Group Policy Information...",
        "SAY:",
        r"SYS:GPResult /R /Z --exestdout=&acn\GPResult.txt",
        "END:"
    ],
    "registry_hives": [
        "SAY:",
        "SAY: [+] Raw Copy Registry Hives...",
        "SAY:",
        r"ACQ:\Reg",
        r"EXE:\TSK\sleuthkit-4.10.0-win32\bin\fcat.exe /Windows/System32/Config/SECURITY \\.\${SYSTEMDRIVE} --exestdout=&acn\Reg\SECURITY",
        r"EXE:\TSK\sleuthkit-4.10.0-win32\bin\fcat.exe /Windows/System32/Config/SOFTWARE \\.\${SYSTEMDRIVE} --exestdout=&acn\Reg\SOFTWARE",
        r"EXE:\TSK\sleuthkit-4.10.0-win32\bin\fcat.exe /Windows/System32/Config/SAM \\.\${SYSTEMDRIVE} --exestdout=&acn\Reg\SAM",
        r"EXE:\TSK\sleuthkit-4.10.0-win32\bin\fcat.exe /Windows/System32/Config/SYSTEM \\.\${SYSTEMDRIVE} --exestdout=&acn\Reg\SYSTEM",
        r"EXE:\TSK\sleuthkit-4.10.0-win32\bin\fcat.exe /Windows/AppCompat/Programs/Amcache.hve \\.\${SYSTEMDRIVE} --exestdout=&acn\Reg\Amcache.hve"
    ],
    "event_viewer_logs" : [
        "SAY:",
        "SAY: [+] Copying (System32) EventViewer Logs...",
        "SAY:",
        r"ACQ:\Evt",
        r"ACQ:\Evt\Sys32",
        r'CPY:"&Win\System32\winevt\Logs\*" "&Acq"',
        "SAY:",
        "SAY: [+] Copying (Sysnative) EventViewer Logs...",
        "SAY:",
        r"ACQ:\Evt\Nativ",
        r'CPY:"&Win\sysnative\winevt\Logs\*" "&Acq"'
    ],
    "srum_hosts_services": [
        "SAY:",
        "SAY: [+] Parsing (System32) Etc Directory, and SRUM...",
        "SAY:",
        r"ACQ:\SYS",
        r"ACQ:\SYS\Sys32",
        r'CPY:"&Win\System32\Drivers\Etc\*" "&Acq"',
        r'CPY:"&Win\System32\sru\SRUDB.dat" "&Acq"',
        "SAY:",
        "SAY: [+] Parsing (Sysnative) Hosts And Services Directory...",
        "SAY:",
        r"ACQ:\SYS\Nativ",
        r'CPY:"&Win\sysnative\Drivers\Etc\*" "&Acq"',
        r'CPY:"&Win\sysnative\sru\SRUDB.dat" "&Acq"',
    ],
    "environment_variables": [
        "SAY:",
        "SAY: [+] Parsing Environment Variables...",
        "SAY:",
        r"ACQ:\SYS",
        r"SYS:CMD /c Set --exestdout=&acn\SYS\EnVar.dat"
    ],
    "patch_list": [
        "SAY:",
        "SAY: [+] Parsing The Patch List...",
        "SAY:",
        r"ACQ:\SYS",
        r"SYS:WMIC qfe list --exestdout=&acn\SYS\QFEList.dat"
    ],
    "running_process_list": [
        "SAY:",
        "SAY: [+] Gathering Running Process List Information...",
        "SAY:",
        r"ACQ:\SYS",
        r"SYS:Tasklist /v --exestdout=&acn\SYS\Tasklist.dat",
        r"SYS:Tasklist /M --exestdout=&acn\SYS\TaskAll.dat",
        r"EXE:\SYS\PSList.exe /accepteula -x --exestdout=&acn\SYS\PSList.dat"
    ],
    "connection_information": [
        "SAY:",
        "SAY: [+] Gathering Connection Information...",
        "SAY:",
        r"ACQ:\SYS",
        r"EXE:\SYS\cports.exe /scomma &Acq\CPorts.csv",
    ],
    "ip_config_information": [
        "SAY:",
        "SAY: [+] Gathering IP Config Information...",
        "SAY:",
        r"ACQ:\SYS",
        r"SYS:IPConfig /all --exestdout=&acn\SYS\IPConfig.dat",
        r"SYS:IPConfig /DisplayDNS --exestdout=&acn\SYS\IPCfgDNS.dat"
    ],
    "arp_information": [
        "SAY:",
        "SAY: [+] Gathering ARP Information...",
        "SAY:",
        r"ACQ:\SYS",
        r"SYS:arp -a --exestdout=&acn\SYS\ArpInfo.dat"
    ],
    "netbios_information": [
        "SAY:",
        "SAY: [+] Gathering NetBIOS Information...",
        "SAY:",
        r"ACQ:\SYS",
        r"CKY:&Win\System32\NBTStat.exe",
        r"SYS:&Win\System32\NBTStat.exe -scn --exestdout=&acn\SYS\NetBios.dat",
        "END:",
        r"CKY:&Win\sysnative\NBTStat.exe",
        r"SYS:&Win\sysnative\NBTStat.exe -scn --exestdout=&acn\SYS\NetBios-2.dat",
        "END:"
    ],
    "open_files_process_information": [
        "SAY:",
        "SAY: [+] Gathering Open Files/Process Information...",
        "SAY:",
        r"ACQ:\SYS",
        r"EXE:\SYS\Handle.exe -a -u -v /accepteula --exestdout=&acn\SYS\OpenFiles.dat"
    ],
    "scheduled_task_information": [
        "SAY:",
        "SAY: [+] Gathering Scheduled Task Information...",
        "SAY:",
        r"ACQ:\SYS",
        r"SYS:At --exestdout=&acn\SYS\SchedTasks.dat",
        r"SYS:Schtasks /query /fo LIST /v --exestdout=&acn\SYS\SchedTasks-2.dat"
    ],
    "system_login_information": [
        "SAY:",
        "SAY: [+] Gathering System Logon Information...",
        "SAY:",
        r"ACQ:\SYS",
        r"EXE:\SYS\PSLoggedon.exe /accepteula --exestdout=&acn\SYS\Logon.dat"
    ],
    "services_information": [
        "SAY:",
        "SAY: [+] Gathering Services Information...",
        "SAY:",
        r"ACQ:\SYS",
        r"SYS:Net Start --exestdout=&acn\SYS\Services.dat",
        r"SYS:sc query type= service state= all --exestdout=&acn\SYS\Services-2.dat",
        r"SYS:Tasklist /SVC --exestdout=&acn\SYS\Services-3.dat"
    ],
    "last_activity_information": [
        "SAY:",
        "SAY: [+] Gathering Last Activity Information...",
        "SAY:",
        r"EXE:\SYS\LastActivityView.exe /scomma &Acq\LastActivity.csv"
    ],
    "user_assist_information": [
        "SAY:",
        "SAY: [+] Gathering User Assist Information...",
        "SAY:",
        r"EXE:\SYS\UserAssistView.exe /scomma &Acq\UserAssist.csv",
    ],
    "autorun_information": [
        "SAY:",
        "SAY: [+] Gathering AutoRun Information...",
        "SAY:",
        r"ACQ:\Arn",
        "SAY:",
        r"EXE:\SYS\Autorunsc.exe /accepteula -a * -c -h --exestdout=&acn\Arn\AutoRun.dat",
        r"EXE:\SYS\Autorunsc.exe /accepteula -cvm --exestdout=&acn\Arn\AutoRun.cpy",
        r"LST:&acn\Arn\AutoRun.cpy",
        'CPY:"&LS8" "&ACQ"'
    ],
    "user_registry": [
        "SAY:",
        "SAY: [+] Gathering Current (Open) User Registry...",
        "SAY:",
        r"ACQ:\Reg",
        r"SYS:Reg Save HKCU &Acq\NTUSER.DAT",
        "SAY:",
        "SAY: [+] Gathering All User Registries...",
        "SAY:",
        r"FOR:${SYSTEMDRIVE}\Users\*\[Nn][Tt][Uu][Ss][Ee][Rr].[Dd][Aa][Tt]",
        r"ACQ:\Reg\&FO2",
        r"EXE:\TSK\sleuthkit-4.10.0-win32\bin\fcat.exe /&FO1/&FO2/&FO3 \\.\${SYSTEMDRIVE} --exestdout=&acn\Reg\&FO2\&FNM"
    ],
    "browser_history": [
        "SAY:",
        "SAY: [+] Now Extracting Browser History...",
        "SAY:",
        r"ACQ:\Brw",
        r"EXE:\SYS\BrowsingHistoryView.exe /scomma &Acq\BrowseHist.csv",
        r"EXE:\SYS\BrowsingHistoryView.exe /shtml &Acq\BrowseHist.htm"
    ],
    "recycle.bin": [
        "SAY:",
        "SAY: [+] Gathering $Recycle.Bin entries (Going 10 Levels Deep)...",
        "SAY:",
        "DSK:Fixed",
        r"ACQ:\RBin",
        r'CPY:"&Dsk:\$Recycle.Bin\**\*" "&Acq"'
    ],
    "powershell_logs": [
        "SAY:",
        "SAY: [+] Copying all User PowerShell Logs...",
        "SAY:",
        r"ACQ:\Psh",
        r'CPY:"${SYSTEMDRIVE}\Users\*\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\*" "&Acq"'
    ],
    "recent_lnk": [
        "SAY:",
        "SAY: [+] Copying all User Recent LNK files...",
        "SAY:",
        r"ACQ:\Lnk",
        r'CPY:"${SYSTEMDRIVE}\Users\*\Desktop\*.lnk" "&Acq"',
        r'CPY:"${SYSTEMDRIVE}\Users\*\AppData\Roaming\Microsoft\Windows\Recent\*.lnk" "&Acq"',

        r"VR2:.\SYS\lnk2csv.py",
        "VR0:py &VR2",
        "CKN:&VR2",
        "Say:",
        "Say:[!] lnk2csv Not Found! Exiting...",
        "Bye:",
        "END:",

        r"VR1:&Acq",
        "Say:",
        "Say:[+] Parsing LNK Files...",
        "Say:",
        r"SYS:&VR0 -f &VR1 -o &VR1\parsed_lnk.csv"
    ],
    "wmi_database": [
        "SAY:",
        "SAY: [+] Copying WMI CIM database files...",
        "SAY:",
        r"ACQ:\WMI",
        r'CPY:"${SYSTEMDRIVE}\Windows\System32\wbem\Repository\*" "&Acq"'
    ],
    "pca": [
        "VER:Windows 10.0.2",
        "SAY: [+] Windows 11 Detected... Copying Program Compatibility Assistant files...",
        "SAY:",
        r"ACQ:\PCA",
        r'CPY:"${SYSTEMDRIVE}\Windows\appcompat\pca\*.txt" "&Acq"',
        "END:"
    ],
    "windows_task_xml_files": [
        "SAY:",
        "SAY: [+] Copying Windows Task XML Files...",
        "SAY:",
        r"ACQ:\Sch",
        r'CPY:"&Win\System32\Tasks\**\*" "&Acq"'
    ],
    "hash": [
        r"VR2:.\SYS\hash.py",
        "VR0:py &VR2",
        "CKN:&VR2",
        "Say:",
        "Say:[!] hash.py Not Found! Exiting...",
        "Bye:",
        "END:",

        "ACQ:\\",
        "VR1:&ACQ",
        "Say:",
        "Say:[+] Hashing Artifacts...",
        "Say:",
        r"SYS:&VR0 -f &VR1 -o &VR1\hash.txt"
    ]
}

def combine_selected_scripts(selected_scripts):
    """
    선택된 스크립트의 내용을 합치는 함수

    Args:
    - selected_scripts (list): 선택된 스크립트 이름들의 리스트

    Returns:
    - str: 합쳐진 스크립트 내용
    """
    combined_content = "\n".join("\n".join(acq_scripts[script]) for script in selected_scripts)
    return combined_content

def save_to_file(filename, content):
    """
    주어진 내용을 파일에 저장하는 함수

    Args:
    - filename (str): 저장할 파일 이름
    - content (str): 파일에 저장할 내용
    """
    with open(filename, "w") as output_file:
        output_file.write(content)
