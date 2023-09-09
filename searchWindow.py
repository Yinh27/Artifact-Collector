from PyQt5.QtWidgets import QMainWindow, QTreeView, QFileSystemModel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import QDir
import os

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

        layout.addWidget(self.tree_view)

        # 검색 기능 추가
        self.search_edit = QLineEdit()
        self.search_button = QPushButton("검색")
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)

        layout.addWidget(self.search_edit)
        layout.addWidget(self.search_button)
        layout.addWidget(self.result_text)

        self.search_button.clicked.connect(self.search_files)

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

        self.result_text.setPlainText(result_text)