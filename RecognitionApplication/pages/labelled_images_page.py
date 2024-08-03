from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem, QMessageBox, QLabel, QFileDialog
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
import os
import pandas as pd
import re
import shutil

class LabelledImagesWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()

        self.setWindowTitle('Labelled Images')
        self.setGeometry(100, 100, 800, 600)
        self.main_window = main_window

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: white;
            }
            QPushButton {
                background-color: #4b4b4b;
                color: white;
                font-size: 14px;
                padding: 10px;
                border: none;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #6b6b6b;
            }
            QListWidget {
                background-color: #3b3b3b;
                color: white;
                font-size: 16px;
                margin: 10px;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #5b5b5b;
            }
            QLabel {
                font-size: 16px;
                color: white;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.folder_list_widget = QListWidget()
        self.folder_list_widget.setIconSize(QSize(100, 100))
        self.layout.addWidget(self.folder_list_widget)
        self.folder_list_widget.itemClicked.connect(self.load_images_from_folder)

        self.image_list_widget = QListWidget()
        self.image_list_widget.setIconSize(QSize(100, 100))
        self.layout.addWidget(self.image_list_widget)

        self.image_display_label = QLabel()
        self.layout.addWidget(self.image_display_label)

        self.load_folders('labelled_images')

        button_layout = QHBoxLayout()
        self.layout.addLayout(button_layout)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)

        show_button = QPushButton("Show")
        show_button.clicked.connect(self.show_item)
        button_layout.addWidget(show_button)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_item)
        button_layout.addWidget(delete_button)

        organize_button = QPushButton("Organize")
        organize_button.clicked.connect(self.organize_images)
        button_layout.addWidget(organize_button)

        self.image_list_widget.itemDoubleClicked.connect(self.item_double_clicked)

    def load_folders(self, root_folder):
        self.folder_list_widget.clear()
        for folder_name in os.listdir(root_folder):
            folder_path = os.path.join(root_folder, folder_name)
            if os.path.isdir(folder_path):
                item = QListWidgetItem(folder_name)
                item.setData(Qt.ItemDataRole.UserRole, folder_path)
                self.folder_list_widget.addItem(item)

    def load_images_from_folder(self, item):
        folder_path = item.data(Qt.ItemDataRole.UserRole)
        self.image_list_widget.clear()

        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                item = QListWidgetItem()
                pixmap = QPixmap(os.path.join(folder_path, filename))
                pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                item.setIcon(QIcon(pixmap))

                item.setData(Qt.ItemDataRole.UserRole, os.path.join(folder_path, filename))
                self.image_list_widget.addItem(item)

    def show_item(self):
        current_item = self.image_list_widget.currentItem()
        if current_item:
            filename = current_item.data(Qt.ItemDataRole.UserRole)
            pixmap = QPixmap(filename)
            self.image_display_label.setPixmap(pixmap.scaled(self.image_display_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
            QMessageBox.information(self, "Selected Item", f"Selected item: {filename}")

    def delete_item(self):
        current_item = self.image_list_widget.currentItem()
        if current_item:
            filename = current_item.data(Qt.ItemDataRole.UserRole)
            reply = QMessageBox.question(self, 'Delete Confirmation',
                                         f"Are you sure you want to delete {filename}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                if os.path.exists(filename):
                    os.remove(filename)
                    self.image_list_widget.takeItem(self.image_list_widget.row(current_item))
                    QMessageBox.information(self, "Delete", f"{filename} has been deleted.")
                else:
                    QMessageBox.warning(self, "Delete", f"{filename} not found.")

    def item_double_clicked(self, item):
        current_item = self.image_list_widget.currentItem()
        if current_item:
            filename = current_item.data(Qt.ItemDataRole.UserRole)
            from .labeling_picture_page import LabellingPic
            self.label_image = LabellingPic(filename, "")
            self.label_image.show()
            self.label_image.closeEvent = lambda event: self.refresh_list()
    
    def refresh_list(self):
        current_item = self.folder_list_widget.currentItem()
        if current_item:
            self.load_images_from_folder(current_item)

    def go_back(self):
        self.main_window.show()
        self.hide()

    def organize_images(self):
        folder_path = 'labelled_images'
        csv_file = 'image_face_names.csv'
        if not os.path.exists(csv_file):
            QMessageBox.warning(self, "Error", "CSV file not found.")
            return

        df = pd.read_csv(csv_file)
        for _, row in df.iterrows():
            image_name = row['image_name']
            face_names = row['face_names'].split(", ")
            for face in face_names:
                person_folder = os.path.join(folder_path, face)
                os.makedirs(person_folder, exist_ok=True)
                src_path = os.path.join(folder_path, image_name)
                dest_path = os.path.join(person_folder, image_name)
                if os.path.exists(src_path) and not os.path.exists(dest_path):
                    shutil.copy(src_path, dest_path)

        self.load_folders(folder_path)
        QMessageBox.information(self, "Organize", "Images have been organized by person.")
