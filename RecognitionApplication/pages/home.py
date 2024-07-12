from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from widgets.scroll_list_example_widget import ScrollListExample
from .unlabeled_options_page import *

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
        self.hide()
        self.labelled_photos_window = ScrollListExample(self)  # Pass the reference to the main window
        self.labelled_photos_window.show()

    def open_unlabelled_options(self):
        self.hide()
        self.unlabelled_options = UnlabelledOptionsPage()
        self.unlabelled_options.show()
