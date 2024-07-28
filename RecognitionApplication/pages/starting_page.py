from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import os

class StartingPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle("Starting Page")
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        self.label = QLabel("Do you want to see the labelled photos or Unlabelled?")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont('Arial', 20))
        main_layout.addWidget(self.label)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.b1 = QPushButton("Labelled")
        self.b1.setFont(QFont('Arial', 16))
        self.b1.clicked.connect(self.show_labelled_photos)  # Connect to show labelled photos method
        button_layout.addWidget(self.b1)

        self.b2 = QPushButton("Unlabelled")
        self.b2.setFont(QFont('Arial', 16))
        self.b2.clicked.connect(self.open_unlabelled_options)
        button_layout.addWidget(self.b2)

        main_layout.addLayout(button_layout)

    def show_labelled_photos(self):
        if not os.path.exists('labelled_images'):
            QMessageBox.warning(self, "No Labelled Images", "Label the images first.")
            return
            
        from .labelled_images_page import LabelledImagesWindow
        self.hide()
        try:
            self.labelled_images_window = LabelledImagesWindow(self)
            self.labelled_images_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def open_unlabelled_options(self):
        from .unlabeled_options_page import UnlabelledOptionsPage
        self.hide()
        self.unlabelled_options = UnlabelledOptionsPage(self)
        self.unlabelled_options.show()
