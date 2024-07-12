from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap,QIcon
from gridfs import GridFS
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon


class AllImagesWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()

        self.setWindowTitle('All Images')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.listWidget = QListWidget()
        self.listWidget.setIconSize(QSize(100, 100))
        self.listWidget.setStyleSheet("QListWidget { margin: 10px; }")

        self.db = db
        self.fs = GridFS(self.db)

        self.load_images()

        self.layout.addWidget(self.listWidget)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.go_back)
        back_button.setStyleSheet("QPushButton { margin: 10px; }")
        self.layout.addWidget(back_button)

    def load_images(self):
        # Fetch all images from GridFS and display them in the list widget
        files = self.fs.find()
        for file in files:
            item = QListWidgetItem()
            pixmap = QPixmap()
            pixmap.loadFromData(file.read())
            pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            item.setIcon(QIcon(pixmap))
            item.setText(file.filename)
            self.listWidget.addItem(item)

    def go_back(self):
        self.close()