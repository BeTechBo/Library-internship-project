from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem, QMessageBox, QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
import os
import pandas as pd
import re

class LabelledImagesWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()

        self.setWindowTitle('Labelled Images')
        self.setGeometry(100, 100, 800, 600)
        self.main_window = main_window

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.listWidget = QListWidget()
        self.listWidget.setIconSize(QSize(100, 100))
        self.listWidget.setStyleSheet("QListWidget { margin: 10px; }")

        self.load_images_from_folder('labelled_images')
        
        self.layout.addWidget(self.listWidget)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.go_back)
        back_button.setStyleSheet("QPushButton { margin: 10px; }")
        self.layout.addWidget(back_button)

        show_button = QPushButton("Show")
        show_button.clicked.connect(self.show_item)
        self.layout.addWidget(show_button)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_item)
        self.layout.addWidget(delete_button)

        # Connect double-click signal to the slot
        self.listWidget.itemDoubleClicked.connect(self.item_double_clicked)

    def refresh_list(self):
        self.listWidget.clear()
        self.load_images_from_folder('labelled_images')
    
    def load_images_from_folder(self, folder_path):
        # Read the CSV file to get image names and face names
        csv_file = 'image_face_names.csv'
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
        else:
            df = pd.DataFrame(columns=['image_name', 'face_names'])

        # Load all images from a folder and display them in the list widget
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                item = QListWidgetItem()
                pixmap = QPixmap(os.path.join(folder_path, filename))
                pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                item.setIcon(QIcon(pixmap))

                widget = QWidget()
                item_layout = QVBoxLayout()

                searching = True
                
                # Get the corresponding face names from the CSV
                face_names = df[df['image_name'] == filename]['face_names'].values
                if face_names:
                    face_names_str = face_names[0]
                    face_names_list = face_names_str.split(", ")
                    if len(face_names_list) == 1:
                        display_text = face_names_list[0]  # Display the face name if only one face
                    else:
                        display_text = filename  # Display image name if more than one face
                        searching = False
                else:
                    display_text = os.path.splitext(filename)[0]  # Default to image name without extension if no entry in CSV
                    # Remove the number in parentheses if present
                    display_text = re.sub(r'\s*\(\d+\)$', '', display_text)

                name_label = QLabel(display_text)
                if searching:
                    search_button = QPushButton("Search")
                    search_button.clicked.connect(lambda _, label=name_label: self.search_person(label.text()))
                item_layout.addWidget(name_label)
                if searching:
                    item_layout.addWidget(search_button)
                widget.setLayout(item_layout)

                # Store the filename in the item for later retrieval
                item.setData(Qt.ItemDataRole.UserRole, filename)

                self.listWidget.addItem(item)
                self.listWidget.setItemWidget(item, widget)

    def search_person(self, name):
        QMessageBox.information(self, "Search", f"Search for: {name}")

    def show_item(self):
        current_item = self.listWidget.currentItem()
        if current_item:
            # Retrieve the filename from the item's data
            filename = current_item.data(Qt.ItemDataRole.UserRole)
            print(f"Selected item filename: {filename}")
            # Optionally, show a message box with the selected item's filename
            QMessageBox.information(self, "Selected Item", f"Selected item: {filename}")

    def delete_item(self):
        current_item = self.listWidget.currentItem()
        if current_item:
            # Retrieve the filename from the item's data
            filename = current_item.data(Qt.ItemDataRole.UserRole)
            reply = QMessageBox.question(self, 'Delete Confirmation',
                                         f"Are you sure you want to delete {filename}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                # Delete the file from the folder
                folder_path = 'labelled_images'
                file_path = os.path.join(folder_path, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.listWidget.takeItem(self.listWidget.row(current_item))
                    QMessageBox.information(self, "Delete", f"{filename} has been deleted.")
                else:
                    QMessageBox.warning(self, "Delete", f"{filename} not found.")

    def item_double_clicked(self, item):
        current_item = self.listWidget.currentItem()
        if current_item:
            # Retrieve the filename from the item's data
            filename = current_item.data(Qt.ItemDataRole.UserRole)
            print(f"Double-clicked on: {filename}")

            from .labeling_picture_page import LabellingPic
            self.label_image = LabellingPic(filename, 'labelled_images')
            self.label_image.show()
            self.label_image.closeEvent = lambda event: self.refresh_list()

    def go_back(self):
        self.main_window.show()
        self.hide()
