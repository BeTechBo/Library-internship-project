from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QInputDialog
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QPen
import sys

class ImageLabel(QWidget):
    def __init__(self, image_path, face_locations):
        super().__init__()
        self.labelPic = QLabel(self)
        self.image = QPixmap(image_path)
        self.face_locations = face_locations
        self.initUI()

    def initUI(self):
        self.setFixedSize(self.image.size())
        self.labelPic.setFixedSize(self.image.size())

    def paintEvent(self, event):
        image_for_drawing = self.image.toImage()
        painter = QPainter(image_for_drawing)

        pen = QPen(QColor(0, 255, 0), 2)
        painter.setPen(pen)
        font = QFont('Arial', 14)
        painter.setFont(font)

        for (top, right, bottom, left) in self.face_locations:
            rect = QRect(left, top, right - left, bottom - top)
            painter.drawRect(rect)
        painter.end()

        self.image = QPixmap.fromImage(image_for_drawing)

        self.labelPic.setPixmap(self.image)
        self.labelPic.resize(self.image.width(), self.image.height())

    def mousePressEvent(self, event):
        for i, (top, right, bottom, left) in enumerate(self.face_locations):
            rect = QRect(left, top, right - left, bottom - top)
            if rect.contains(event.pos()):
                self.edit_name(i)
                return

    def edit_name(self, index):
        name, ok = QInputDialog.getText(self, 'Edit Name', 'Enter the name:')
        if ok and name:
            print(f"Name entered: {name} for face at index {index}")
            # Handle updating labels or saving names as needed