from PyQt6.QtWidgets import QLabel, QWidget, QInputDialog, QMessageBox
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QPen, QImage
from services.database import Database
import face_recognition
import numpy as np

class ImageLabel(QWidget):
    def __init__(self, image_array, face_locations, face_encodings):
        super().__init__()
        self.labelPic = QLabel(self)
        
        # Convert numpy array to QImage
        height, width, channel = image_array.shape
        bytes_per_line = 3 * width
        qimage = QImage(image_array.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        
        # Convert QImage to QPixmap
        self.image = QPixmap(qimage)
        
        self.face_locations = face_locations
        self.face_encodings = face_encodings  # for the database
        self.initUI()

    def initUI(self):
        self.setFixedSize(self.image.size())
        self.labelPic.setFixedSize(self.image.size())
        self.labelPic.setPixmap(self.image)
        self.labelPic.resize(self.image.width(), self.image.height())

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

    def get_all_face_encodings(self, faces):
        encodings = []
        for document in faces.find({}):  # Find all documents in the collection
            face_encoding_list = document['face_encoding']
            face_encoding_np = np.array(face_encoding_list)  # Convert list to numpy array
            encodings.append(face_encoding_np)
        return encodings
    
    def edit_name(self, index):
        database = Database()
        db =  database.client['all_faces']
        faces = db['faces_data']
        
        #find if the face is already exist in our database or not
        face_encoding = self.face_encodings[index]
        all_faces_encodings = self.get_all_face_encodings(faces)
        compare_faces = face_recognition.compare_faces(all_faces_encodings, face_encoding, tolerance=0.8)
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
