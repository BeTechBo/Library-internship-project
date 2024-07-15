from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class SlideshowWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.image_label = QLabel("No Image")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedSize(600, 400)  # Fixed size for displaying images
        self.image_label.setScaledContents(True)
        self.image_paths = []
        self.current_index = 0

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.image_label)

        self.prev_button = QPushButton("Before")
        self.prev_button.clicked.connect(self.prev_image)
        self.prev_button.setEnabled(False)  # Initially disable prev button

        self.next_button = QPushButton("After")
        self.next_button.clicked.connect(self.next_image)
        self.next_button.setEnabled(False)  # Initially disable next button

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addStretch(1)
        button_layout.addWidget(self.next_button)

        self.layout().addLayout(button_layout)

    def set_image_paths(self, image_paths):
        self.image_paths = image_paths
        if self.image_paths:
            self.show_image()
            self.update_buttons()

    def show_image(self):
        pixmap = QPixmap(self.image_paths[self.current_index])
        pixmap = pixmap.scaledToWidth(self.image_label.width())  # Scale pixmap to fit label width
        self.image_label.setPixmap(pixmap)

    def next_image(self):
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            self.show_image()
            self.update_buttons()

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image()
            self.update_buttons()

    def update_buttons(self):
        self.prev_button.setEnabled(self.current_index > 0)
        self.next_button.setEnabled(self.current_index < len(self.image_paths) - 1)
