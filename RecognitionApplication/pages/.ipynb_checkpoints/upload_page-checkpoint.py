import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QTabWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from gridfs import GridFS
from services.database import Database

class UploadPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.database = Database()
        self.client = self.database.client
        self.setWindowTitle("Image Upload Example")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.tab_widget = QTabWidget()
        self.tab_1 = QWidget()
        self.tab_2 = QWidget()

        self.upload_dir = os.path.join(os.getcwd(), 'uploaded_images')
        os.makedirs(self.upload_dir, exist_ok=True)

        self.db = self.client['all_images']
        self.fs = GridFS(self.db)

        self.option_upload_single()
        self.option_upload_multiple()

        self.tab_widget.addTab(self.tab_1, "Tab 1")
        self.tab_widget.addTab(self.tab_2, "Tab 2")
        self.layout.addWidget(self.tab_widget)

        self.return_back = QPushButton("Return Home")
        self.return_back.clicked.connect(self.return_home)
        self.layout.addWidget(self.return_back)

    def option_upload_single(self):
        layout = QFormLayout()
        self.upload_button_single = QPushButton("Upload Image")
        self.upload_button_single.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_button_single)

        self.image_label_single = QLabel("No Image Uploaded")
        self.image_label_single.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label_single)

        self.tab_1.setLayout(layout)

    def option_upload_multiple(self):
        layout = QFormLayout()
        self.upload_button_multiple = QPushButton("Upload Multiple Images")
        self.upload_button_multiple.clicked.connect(self.upload_images)
        layout.addWidget(self.upload_button_multiple)

        self.tab_2.setLayout(layout)

    def upload_image(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(self, "Select an Image", "", 
                                                       "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
            if file_name:
                if self.image_exists(file_name):
                    QMessageBox.warning(self, "Duplicate Image", "This image already exists in the database.")
                else:
                    pixmap = QPixmap(file_name)
                    self.image_label_single.setPixmap(pixmap.scaled(self.image_label_single.size(), Qt.AspectRatioMode.KeepAspectRatio))
                    self.image_label_single.setText("")
                    image_id = self.save_image(file_name)
                    # Optionally store image_id in your database or use it as needed
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def upload_images(self):
        try:
            file_names, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", 
                                                         "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)")
            if file_names:
                new_files = [file_name for file_name in file_names if not self.image_exists(file_name)]
                image_ids = [self.save_image(file_name) for file_name in new_files]
                if image_ids:
                    QMessageBox.information(self, "Images Uploaded", f"Uploaded {len(image_ids)} images.")
                if len(new_files) < len(file_names):
                    QMessageBox.warning(self, "Duplicate Images", f"{len(file_names) - len(new_files)} images were duplicates and were not uploaded.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def save_image(self, file_name):
        try:
            with open(file_name, 'rb') as image_file:
                image_id = self.fs.put(image_file, filename=os.path.basename(file_name))
            print(f"Image saved to MongoDB GridFS with id: {image_id}")
            return image_id  # Return the image_id for reference
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save image: {e}")

    def image_exists(self, file_name):
        try:
            filename = os.path.basename(file_name)
            return self.fs.exists({'filename': filename})
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to check if image exists: {e}")
            return False

    def return_home(self):
        self.hide()
        from .starting_page import StartingPage
        self.start = StartingPage()
        self.start.show()
