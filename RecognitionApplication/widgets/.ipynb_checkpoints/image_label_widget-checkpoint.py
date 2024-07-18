from PyQt6.QtWidgets import QLabel, QWidget, QInputDialog, QMessageBox, QSizePolicy
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QPen, QImage, QBrush
from services.database import Database
import face_recognition
import numpy as np

class ImageLabel(QWidget):
    def __init__(self, image_array, face_locations, face_encodings):
        super().__init__()
        self.face_locations = face_locations
        self.face_encodings = face_encodings  # for the database
        self.face_names = ["Unknown"] * len(face_locations)  # Initialize with "Unknown"

        # Convert numpy array to QImage
        height, width, channel = image_array.shape
        bytes_per_line = 3 * width
        qimage = QImage(image_array.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        
        # Convert QImage to QPixmap
        self.image = QPixmap(qimage)
        
        self.initUI()
        self.load_names()

    def initUI(self):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(100, 100)  # Set minimum size to ensure it is usable

    def paintEvent(self, event):
        # Scale the image to fit the widget size
        scaled_image = self.image.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio)

        # Draw the scaled image
        painter = QPainter(self)
        painter.drawPixmap(0, 0, scaled_image)

        # Draw rectangles and names
        painter.setPen(QPen(Qt.GlobalColor.green, 2))
        painter.setFont(QFont('Arial', 14))

        # Get the scale factors
        width_scale = scaled_image.width() / self.image.width()
        height_scale = scaled_image.height() / self.image.height()

        self.scaled_face_locations = []
        for top, right, bottom, left in self.face_locations:
            # Scale face locations to fit the scaled image
            scaled_top = top * height_scale
            scaled_right = right * width_scale
            scaled_bottom = bottom * height_scale
            scaled_left = left * width_scale

            self.scaled_face_locations.append(QRect(int(scaled_left), int(scaled_top), int(scaled_right - scaled_left), int(scaled_bottom - scaled_top)))
            painter.drawRect(self.scaled_face_locations[-1])
            painter.drawText(self.scaled_face_locations[-1].left(), self.scaled_face_locations[-1].top() - 10, self.face_names[self.scaled_face_locations.index(self.scaled_face_locations[-1])])

        painter.end()

    def mousePressEvent(self, event):
        click_x = event.position().x()
        click_y = event.position().y()

        for i, rect in enumerate(self.scaled_face_locations):
            if rect.contains(click_x, click_y):
                self.edit_name(i)
                return

    def get_all_face_encodings(self, faces):
        encodings = []
        for document in faces.find({}):  # Find all documents in the collection
            face_encoding_list = document['face_encoding']
            face_encoding_np = np.array(face_encoding_list)  # Convert list to numpy array
            encodings.append(face_encoding_np)
        return encodings

    def load_names(self):
        database = Database()
        db = database.client['all_faces']
        faces = db['faces_data']
        all_faces_encodings = self.get_all_face_encodings(faces)
        for i, face_encoding in enumerate(self.face_encodings):
            compare_faces = face_recognition.compare_faces(all_faces_encodings, face_encoding, tolerance=0.6)
            if any(compare_faces):
                matching_index = compare_faces.index(True)
                self.face_names[i] = faces.find()[matching_index]['name']

    def edit_name(self, index):
        database = Database()
        db = database.client['all_faces']
        faces = db['faces_data']
        
        # Find if the face is already in our database
        face_encoding = self.face_encodings[index]
        all_faces_encodings = self.get_all_face_encodings(faces)
        compare_faces = face_recognition.compare_faces(all_faces_encodings, face_encoding, tolerance=0.55)
        if any(compare_faces):
            matching_index = compare_faces.index(True)  # Get the index of the first match
            matched_name = faces.find()[matching_index]['name']
            reply = QMessageBox.question(self, 'Match Found', f"The name for this person is {matched_name}. Do you want to edit it?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return
            # Delete the document with matched_name if answer = yes
            faces.delete_one({'name': matched_name})
        
        name, ok = QInputDialog.getText(self, 'Edit Name', 'Enter the name:')
        if ok and name:
            document = {
                "name": name,
                "face_encoding": face_encoding.tolist()
            }
            faces.insert_one(document)
            self.face_names[index] = name  # Update the name for the face
            self.update()  # Repaint the widget to show the updated name
