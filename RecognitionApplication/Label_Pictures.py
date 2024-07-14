import face_recognition
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

    

class LabellingPic(QMainWindow):
    def __init__(self, photo_name):
        super().__init__()
        self.PN = photo_name
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle("Labelling Pictures")
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the main window
        main_layout = QVBoxLayout(central_widget)

        # Set margins for the layout (left, top, right, bottom)
        main_layout.setContentsMargins(10, 40, 10, 100)

        # Label
        self.label = QLabel()
        self.label.setText("Label the Pictures below: ")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont('Arial', 20))
        main_layout.addWidget(self.label)

        # Load image and detect faces
        image_path = "D:\Internships_work\Library internship\pyqt\\temp\\"
        full_path = image_path + self.PN
        print(full_path)
        image = face_recognition.load_image_file(full_path)
        face_locations = face_recognition.face_locations(image)

        # Create custom widget for displaying image with rectangles
        self.image_label = ImageLabel(full_path, face_locations)
        
        # Center the image_label widget using a horizontal layout
        hbox_layout = QHBoxLayout()
        hbox_layout.addStretch(1)
        hbox_layout.addWidget(self.image_label)
        hbox_layout.addStretch(1)

        # Add the horizontal layout to the main layout
        main_layout.addLayout(hbox_layout)


# def window():
#     app = QApplication(sys.argv)
#     win = LabellingPic()
#     win.show()
#     sys.exit(app.exec())


# if __name__ == "__main__":
#     window()