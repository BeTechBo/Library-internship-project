import face_recognition
from widgets.image_label_widget import ImageLabel
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QSizePolicy


class LabellingPic(QMainWindow):
    def __init__(self, image_array):
        super().__init__()
        self.image_array = image_array
        self.setGeometry(200, 200, 800, 600)  # Adjust window size as needed
        self.setWindowTitle("Labelling Pictures")
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the main window
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 40, 10, 10)

        # Label
        self.label = QLabel()
        self.label.setText("Label the Pictures below: ")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont('Arial', 20))
        main_layout.addWidget(self.label)

        # Load image and detect faces
        face_locations = face_recognition.face_locations(self.image_array)
        face_encodings = face_recognition.face_encodings(self.image_array)  # for database

        # Create custom widget for displaying image with rectangles
        self.image_label = ImageLabel(self.image_array, face_locations, face_encodings)
        
        # Add the image_label widget to the main layout
        main_layout.addWidget(self.image_label)

        # Set size policy to expand with window size
        self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)