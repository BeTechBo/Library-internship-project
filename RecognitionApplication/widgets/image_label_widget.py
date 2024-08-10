from PyQt6.QtWidgets import QLabel, QWidget, QInputDialog, QMessageBox, QSizePolicy, QVBoxLayout
from PyQt6.QtCore import Qt, QRect, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QPainter, QPen, QImage, QBrush
import face_recognition
import numpy as np
import pandas as pd
import os
import shutil

class ImageLabel(QWidget):    
    image_loaded = pyqtSignal(bool)  # Signal to emit after loading names

    def __init__(self, image_path, face_locations, face_encodings):
        super().__init__()
        self.image_path = image_path
        self.dest_path_csv_file = image_path
        self.labelPic = QLabel(self)
        self.original_image = QPixmap(image_path)
        self.face_locations = face_locations
        self.face_encodings = face_encodings
        self.face_names = ["Unknown"] * len(face_locations)  # Initialize with "Unknown"
        self.move_image = False
        
        self.initUI()
        self.load_names()

    def initUI(self):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout = QVBoxLayout()
        layout.addWidget(self.labelPic)
        self.setLayout(layout)
        self.update_image()

    def update_image(self):
        # Scale the image to fit the label size
        scaled_image = self.original_image.scaled(self.labelPic.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.labelPic.setPixmap(scaled_image)
        self.labelPic.adjustSize()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_image()

    def paintEvent(self, event):
        # Create a COPY for drawing
        image_copy = self.original_image.copy() 

        scaled_image = image_copy.scaled(self.labelPic.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation) 

        # Draw the scaled image
        image_for_drawing = scaled_image.toImage()
        painter = QPainter(image_for_drawing)

        # Draw rectangles and names
        painter.setPen(QPen(Qt.GlobalColor.green, 2))
        painter.setFont(QFont('Arial', 14))

        # Get the scale factors
        scaled_image_size = scaled_image.size()
        width_scale = scaled_image_size.width() / self.original_image.width()
        height_scale = scaled_image_size.height() / self.original_image.height()

        self.scaled_face_locations = []
        for index, (top, right, bottom, left) in enumerate(self.face_locations):
            # Scale face locations to fit the scaled image
            scaled_top = int(top * height_scale)
            scaled_right = int(right * width_scale)
            scaled_bottom = int(bottom * height_scale)
            scaled_left = int(left * width_scale)

            self.scaled_face_locations.append(QRect(scaled_left, scaled_top, scaled_right - scaled_left, scaled_bottom - scaled_top))

            # White Background Behind Text
            text_rect = painter.boundingRect(self.scaled_face_locations[-1], Qt.AlignmentFlag.AlignLeft, self.face_names[self.scaled_face_locations.index(self.scaled_face_locations[-1])])
            text_rect.setHeight(text_rect.height() + 7)
            text_rect.moveTop(text_rect.top() - text_rect.height() - 5) # 5 is a padding value

            painter.drawRect(self.scaled_face_locations[-1])

            painter.fillRect(text_rect, QBrush(Qt.GlobalColor.white))

            painter.drawText(self.scaled_face_locations[-1].left(), self.scaled_face_locations[-1].top() - 10, self.face_names[index])  # Correctly use index

        painter.end()
        
        # Set the scaled image on the label
        self.labelPic.setPixmap(QPixmap.fromImage(image_for_drawing))
        self.labelPic.resize(self.labelPic.pixmap().size())

    def mousePressEvent(self, event):
        click_x = int(event.position().x()) 
        click_y = int(event.position().y())

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
        # If the image does not contain any faces then return
        if len(self.face_locations) < 1:
            return
        
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

        self.rename_images()
        self.save_image_names()  # Save image and face names to CSV
        
        # Move the image if there are no "Unknown" names
        if not any(name == "Unknown" for name in self.face_names):
            self.move_image = True
        self.image_loaded.emit(self.move_image)  # Emit signal with the value


    def rename_images(self):
        item_text = os.path.basename(self.image_path)
        src_path = os.path.join('uploaded_images', item_text)

        # Check if the item exists in the uploaded_images folder
        if not os.path.exists(src_path):
            return
        
        dest_path = os.path.join('labelled_images', item_text)
    
        # Create the folder if it doesn't exist
        labelled_folder = 'labelled_images'
        if not os.path.exists(labelled_folder):
            os.makedirs(labelled_folder)
    
        # Check if the same content image already exists
        same_content = False
        for dest_filename in os.listdir('labelled_images'):
            full_dest_path = os.path.join('labelled_images', dest_filename)
            if open(src_path, 'rb').read() == open(full_dest_path, 'rb').read():
                same_content = True
                break
    
        if os.path.exists(dest_path) and not same_content:
            base_name, extension = os.path.splitext(item_text)
            counter = 1
            new_dest_path = os.path.join('labelled_images', f"{base_name} ({counter}){extension}")
            while os.path.exists(new_dest_path):
                counter += 1
                new_dest_path = os.path.join('labelled_images', f"{base_name} ({counter}){extension}")
            dest_path = new_dest_path
            self.dest_path_csv_file = dest_path

    def edit_name(self, index):
        csv_file = 'faces_data.csv'  # Path to your CSV file
        try:
            df = pd.read_csv(csv_file)
        except (pd.errors.EmptyDataError, FileNotFoundError):
            df = pd.DataFrame(columns=['name', 'face_encoding'])

        images_csv_file = 'image_face_names.csv'
        try:
            im_df = pd.read_csv(images_csv_file)
        except (pd.errors.EmptyDataError, FileNotFoundError):
            df = pd.DataFrame(columns=['image_name', 'face_names'])
    
        # Find if the face is already in our CSV
        face_encoding = self.face_encodings[index]
        all_faces_encodings = self.get_all_face_encodings(csv_file)
        matched_name = None
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
            if matched_name:
                # Replace the old name with the new name in all entries
                im_df['face_names'] = im_df['face_names'].apply(lambda x: ', '.join([name if each_name.strip() == matched_name else each_name.strip() for each_name in x.split(',')]))
                im_df.to_csv(images_csv_file, index=False)
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
            self.save_image_names()  # Save image and face names to CSV

    def save_image_names(self):
        image_name = os.path.basename(self.dest_path_csv_file)  # Get the image file name
        data = {
            "image_name": image_name,
            "face_names": ", ".join(self.face_names)  # Join all face names into a single string
        }

        csv_file = "image_face_names.csv"
        
        # Check if the file exists
        if os.path.exists(csv_file):
            # Read the existing data
            df = pd.read_csv(csv_file)

            # Check if the image name already exists
            if image_name in df['image_name'].values:
                # Update the existing row
                df.loc[df['image_name'] == image_name, 'face_names'] = data['face_names']
            else:
                # Append a new row
                df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        else:
            # Create a new DataFrame if the file does not exist
            df = pd.DataFrame([data])

        # Write the DataFrame to the CSV file
        df.to_csv(csv_file, index=False)
        
        print(f"Saved image names for {image_name}")  # Debug print
