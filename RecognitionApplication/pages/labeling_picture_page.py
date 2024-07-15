import face_recognition
from widgets.image_label_widget import ImageLabel
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QInputDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

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
        # image_path = "C:\\Users\\user\\Downloads\\Library_Internship\\GitHub\\LibraryFacialRecognition\\RecognitionApplication\\uploaded_images\\"
        full_path = image_path + self.PN
        print(full_path)
        image = face_recognition.load_image_file(full_path)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image) #for database

        # Create custom widget for displaying image with rectangles
        self.image_label = ImageLabel(full_path, face_locations, face_encodings)
        
        # Center the image_label widget using a horizontal layout
        hbox_layout = QHBoxLayout()
        hbox_layout.addStretch(1)
        hbox_layout.addWidget(self.image_label)
        hbox_layout.addStretch(1)

        # Add the horizontal layout to the main layout
        main_layout.addLayout(hbox_layout)