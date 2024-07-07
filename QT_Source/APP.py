import sys
import os
import shutil

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pyqt_slideshow import SlideShow  


class Upload_page(QMainWindow):
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

        self.return_back = QPushButton("Return Home")
        self.return_back.clicked.connect(self.return_home)
        self.layout.addWidget(self.return_back)

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
        self.slideshow.setMinimumSize(600, 400)  # Example: Set minimum size for slideshow
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
    
    def return_home(self):
        self.hide()
        self.start = StartingPage()
        self.start.show()


class StartingPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle("Starting Page")
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the main window
        main_layout = QVBoxLayout(central_widget)

        # Label
        self.label = QLabel()
        self.label.setText("Do you want to see the labelled photos or Unlabelled?")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont('Arial', 20))
        main_layout.addWidget(self.label)

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Aligns the QHBoxLayout center within its parent layout
        button_layout.setContentsMargins(40, 100, 40, 320)  # Sets margins around the QHBoxLayout
        button_layout.setSpacing(250)  # Sets spacing between buttons

        self.b1 = QPushButton()
        self.b1.setText("Labelled")
        self.b1.clicked.connect(self.clicked1)
        self.b1.setFont(QFont('Arial', 16))
        button_layout.addWidget(self.b1)

        self.b2 = QPushButton()
        self.b2.setText("Unlabelled")
        self.b2.clicked.connect(self.open_upload)
        self.b2.setFont(QFont('Arial', 16))
        button_layout.addWidget(self.b2)

        # Add the horizontal layout to the main vertical layout
        main_layout.addLayout(button_layout)

    def clicked1(self):
        self.b1.setText("You pressed the Labelled button")
        self.b1.adjustSize()

    def clicked2(self):
        self.b2.setText("You pressed the Unlabelled button")
        self.b2.adjustSize()
    
    def open_upload(self):
        self.hide()
        self.uploadP = Upload_page()
        self.uploadP.show() 
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = StartingPage()
    main_window.show()
    sys.exit(app.exec_())
