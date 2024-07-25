from PyQt6.QtWidgets import QLabel, QWidget, QInputDialog, QMessageBox, QSizePolicy
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QPen, QImage, QBrush
import face_recognition
import numpy as np
import pandas as pd
import os

class ImageLabel(QWidget):
    def __init__(self, image_array, face_locations, face_encodings):
        super().__init__()
        self.face_locations = face_locations
        self.face_encodings = face_encodings
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
        for index, (top, right, bottom, left) in enumerate(self.face_locations):
            # Scale face locations to fit the scaled image
            scaled_top = top * height_scale
            scaled_right = right * width_scale
            scaled_bottom = bottom * height_scale
            scaled_left = left * width_scale

            self.scaled_face_locations.append(QRect(int(scaled_left), int(scaled_top), int(scaled_right - scaled_left), int(scaled_bottom - scaled_top)))
            painter.drawRect(self.scaled_face_locations[-1])
            painter.drawText(self.scaled_face_locations[-1].left(), self.scaled_face_locations[-1].top() - 10, self.face_names[index])  # Correctly use the index

        painter.end()

    def mousePressEvent(self, event):
        click_x = event.position().x()
        click_y = event.position().y()

        for i, rect in enumerate(self.scaled_face_locations):
            if rect.contains(click_x, click_y):
                self.edit_name(i)
                return

    def get_all_face_encodings(self, csv_file):
        try:
            df = pd.read_csv(csv_file)
            if df.empty:
                return []
            encodings = [np.array(eval(encoding)) for encoding in df['face_encoding']]
            return encodings
        except (pd.errors.EmptyDataError, FileNotFoundError):
            return []

    def load_names(self):
        csv_file = 'faces_data.csv'  # Path to your CSV file
        if not os.path.exists(csv_file):
            return

        df = pd.read_csv(csv_file)
        if df.empty:
            return

        all_faces_encodings = self.get_all_face_encodings(csv_file)
        for i, face_encoding in enumerate(self.face_encodings):
            if all_faces_encodings:
                distances = face_recognition.face_distance(all_faces_encodings, face_encoding)
                best_match_index = np.argmin(distances)
                if distances[best_match_index] <= 0.6:
                    self.face_names[i] = df.iloc[best_match_index]['name']
        print("Loaded names:", self.face_names)  # Debug print

    def edit_name(self, index):
        csv_file = 'faces_data.csv'  # Path to your CSV file
        try:
            df = pd.read_csv(csv_file)
        except (pd.errors.EmptyDataError, FileNotFoundError):
            df = pd.DataFrame(columns=['name', 'face_encoding'])
    
        # Find if the face is already in our CSV
        face_encoding = self.face_encodings[index]
        all_faces_encodings = self.get_all_face_encodings(csv_file)
        if all_faces_encodings:
            distances = face_recognition.face_distance(all_faces_encodings, face_encoding)
            best_match_index = np.argmin(distances)
            if distances[best_match_index] <= 0.55:
                matched_name = df.iloc[best_match_index]['name']
                reply = QMessageBox.question(self, 'Match Found', f"The name for this person is {matched_name}. Do you want to edit it?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.No:
                    return
                # Delete the row with the matched name if answer is yes
                df = df.drop(best_match_index).reset_index(drop=True)
       
        name, ok = QInputDialog.getText(self, 'Edit Name', 'Enter the name:')
        if ok and name:
            new_entry = pd.DataFrame({
                "name": [name],
                "face_encoding": [face_encoding.tolist()]
            })
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(csv_file, index=False)
            self.face_names[index] = name  # Update the name for the face
            print(f"Updated name at index {index}: {name}")  # Debug print
            self.load_names()  # Reload names from CSV after update
            self.update()  # Repaint the widget to show the updated name
