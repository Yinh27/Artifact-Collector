from PyQt5.QtWidgets import QMainWindow, QTreeView, QFileSystemModel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTextEdit, QAction
from PyQt5.QtCore import QDir
import os
from fileWindow import FileWindow

class FileSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.show()
        
    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("파일 검색기")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        # 파일 시스템 모델 생성 및 루트 경로 설정 (현재 디렉토리)
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())

        # 트리 뷰 생성 및 모델 설정
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(QDir.currentPath()))
        self.tree_view.doubleClicked.connect(self.open_file)

        layout.addWidget(self.tree_view)

        # 검색 기능 추가
        self.search_edit = QLineEdit()
        self.search_button = QPushButton("검색")
        self.search_result_text = QTextEdit()
        self.search_result_text.setReadOnly(True)

        layout.addWidget(self.search_edit)
        layout.addWidget(self.search_button)
        layout.addWidget(self.search_result_text)

        self.search_button.clicked.connect(self.search_files)
        
        menubar = self.menuBar()
        file_menu = menubar.addMenu('파일')
        open_action = QAction('열기', self)
        #open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)

    def search_files(self):
        keyword = self.search_edit.text()
        if not keyword:
            return

        result_text = "검색 결과:\n"

        # 현재 디렉토리와 그 하위 디렉토리에서 검색
        for dirpath, dirnames, filenames in os.walk(QDir.currentPath()):
            for filename in filenames:
                if keyword in filename:
                    result_text += os.path.join(dirpath, filename) + "\n"

        self.search_result_text.setPlainText(result_text)
        
    def open_file(self, index):
        file_path = self.model.filePath(index)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_contents = file.read()
                    self.contents = FileWindow(file_contents)
            except UnicodeDecodeError:
                try:
                    with open(file_path, 'r', encoding='ANSI') as file:
                        file_contents = file.read()
                    self.contents = FileWindow(file_contents)
                except Exception as e:
                    self.search_result_text.setPlainText(f"파일을 열 수 없음: {str(e)}")
            except Exception as e:
                self.search_result_text.setPlainText(f"파일을 열 수 없음: {str(e)}")