import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from pyqt_slideshow import SlideShow  
import os
import shutil

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Upload Example")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.tab_widget = QTabWidget()
        self.tab_1 = QWidget()
        self.tab_2 = QWidget()
        self.option_upload_multiple()
        self.option_upload_single()

        self.tab_widget.addTab(self.tab_1, "Tab 1")
        self.tab_widget.addTab(self.tab_2, "Tab 2")
        self.layout.addWidget(self.tab_widget)

    def option_upload_single(self):
        
        layout = QFormLayout()
        self.upload_button = QPushButton("Upload Image")
        self.upload_button.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_button)

        self.image_label_2 = QLabel("No Image Uploaded")
        self.image_label_2.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label_2)

        self.upload_dir = os.path.join(os.getcwd(), 'uploaded_images')
        os.makedirs(self.upload_dir, exist_ok=True)
        self.tab_1.setLayout(layout)

    def option_upload_multiple(self):
        
        layout = QFormLayout()
        self.upload_button = QPushButton("Upload Multiple Images")
        self.upload_button.clicked.connect(self.upload_images)
        layout.addWidget(self.upload_button)
        self.slideshow = SlideShow()
        self.slideshow.setMinimumSize(600, 400)  
        layout.addWidget(self.slideshow)
        self.upload_dir = os.path.join(os.getcwd(), 'uploaded_images')
        os.makedirs(self.upload_dir, exist_ok=True)
        self.tab_2.setLayout(layout)

    def upload_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Select an Image", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)", options=options)
        if file_name:
            pixmap = QPixmap(file_name)
            self.image_label_2.setPixmap(pixmap.scaled(self.image_label_2.size(), Qt.KeepAspectRatio))
            self.image_label_2.setText("")
            base_name = os.path.basename(file_name)
            dest_path = os.path.join(self.upload_dir, base_name)
            shutil.copy(file_name, dest_path)
            print(f"Image saved to {dest_path}")

    def upload_images(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select Images", "",
                                                     "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)", options=options)
        if file_names:
            image_paths = []
            for file_name in file_names:
                base_name = os.path.basename(file_name)
                dest_path = os.path.join(self.upload_dir, base_name)
                shutil.copy(file_name, dest_path)
                image_paths.append(dest_path)
                print(f"Image saved to {dest_path}")

            if image_paths:
                self.update_slideshow(image_paths)

    def update_slideshow(self, image_paths):
        self.slideshow.setFilenames(image_paths)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
