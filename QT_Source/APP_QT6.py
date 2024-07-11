import sys
import os
import shutil
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QTabWidget, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont, QIcon
import pymongo
from gridfs import GridFS

from pymongo import MongoClient
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon


class AllImagesWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()

        self.setWindowTitle('All Images')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.listWidget = QListWidget()
        self.listWidget.setIconSize(QSize(100, 100))
        self.listWidget.setStyleSheet("QListWidget { margin: 10px; }")

        self.db = db
        self.fs = GridFS(self.db)

        self.load_images()

        self.layout.addWidget(self.listWidget)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.go_back)
        back_button.setStyleSheet("QPushButton { margin: 10px; }")
        self.layout.addWidget(back_button)

    def load_images(self):
        # Fetch all images from GridFS and display them in the list widget
        files = self.fs.find()
        for file in files:
            item = QListWidgetItem()
            pixmap = QPixmap()
            pixmap.loadFromData(file.read())
            pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            item.setIcon(QIcon(pixmap))
            item.setText(file.filename)
            self.listWidget.addItem(item)

    def go_back(self):
        self.close()

class SlideshowWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.image_label = QLabel("No Image")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedSize(600, 400)  # Fixed size for displaying images
        self.image_label.setScaledContents(True)
        self.image_paths = []
        self.current_index = 0

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.image_label)

        self.prev_button = QPushButton("Before")
        self.prev_button.clicked.connect(self.prev_image)
        self.prev_button.setEnabled(False)  # Initially disable prev button

        self.next_button = QPushButton("After")
        self.next_button.clicked.connect(self.next_image)
        self.next_button.setEnabled(False)  # Initially disable next button

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addStretch(1)
        button_layout.addWidget(self.next_button)

        self.layout().addLayout(button_layout)

    def set_image_paths(self, image_paths):
        self.image_paths = image_paths
        if self.image_paths:
            self.show_image()
            self.update_buttons()

    def show_image(self):
        pixmap = QPixmap(self.image_paths[self.current_index])
        pixmap = pixmap.scaledToWidth(self.image_label.width())  # Scale pixmap to fit label width
        self.image_label.setPixmap(pixmap)

    def next_image(self):
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            self.show_image()
            self.update_buttons()

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image()
            self.update_buttons()

    def update_buttons(self):
        self.prev_button.setEnabled(self.current_index > 0)
        self.next_button.setEnabled(self.current_index < len(self.image_paths) - 1)

class ScrollListExample(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window  # Reference to the main window

        self.setWindowTitle('Scrollable List Example')
        self.setGeometry(100, 100, 400, 600)

        layout = QVBoxLayout()

        # Heading
        heading = QLabel("Labeled Photos")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading.setFont(QFont('Arial', 20))
        heading.setStyleSheet("QLabel { color: blue; margin: 20px; }")
        layout.addWidget(heading)

        self.listWidget = QListWidget()
        self.listWidget.setStyleSheet("QListWidget { margin: 10px; }")

        # Connect to MongoDB
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client['photo_database']
        fs = GridFS(db)

        # Fetch data from MongoDB
        people = db.people.find()

        for person in people:
            item = QListWidgetItem()
            widget = QWidget()
            h_layout = QHBoxLayout()

            label_name = QLabel(person['name'])
            label_name.setFont(QFont('Arial', 14))
            label_image = QLabel()

            # Load image from MongoDB GridFS
            image_id = person['image_id']
            image_data = fs.get(image_id).read()
            pixmap = QPixmap()
            if pixmap.loadFromData(image_data):
                pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            else:
                # Placeholder image if the file is not found
                pixmap = QPixmap(100, 100)
                pixmap.fill(QColor('gray'))
                label_image.setText("Image not found")

            label_image.setPixmap(pixmap)

            search_button = QPushButton("Search")
            search_button.clicked.connect(self.on_search_button_clicked)
            search_button.setStyleSheet("QPushButton { margin-left: 10px; }")

            h_layout.addWidget(label_image)
            h_layout.addWidget(label_name)
            h_layout.addWidget(search_button)
            widget.setLayout(h_layout)

            item.setSizeHint(widget.sizeHint())
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, widget)

        layout.addWidget(self.listWidget)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.go_back)  # Go back to the main window
        back_button.setStyleSheet("QPushButton { margin: 10px; }")
        layout.addWidget(back_button)

        self.setLayout(layout)

    def on_search_button_clicked(self):
        # Placeholder for search button functionality
        print("Search button clicked")

    def go_back(self):
        self.hide()
        self.main_window.show()

class UploadPage(QMainWindow):
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

        self.upload_dir = os.path.join(os.getcwd(), 'uploaded_images')
        os.makedirs(self.upload_dir, exist_ok=True)

        self.client = MongoClient('mongodb://localhost:27017/')
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
                image_ids = [self.save_image(file_name) for file_name in file_names]
                if image_ids:
                    QMessageBox.information(self, "Images Uploaded", f"Uploaded {len(image_ids)} images.")
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

    def return_home(self):
        self.hide()
        # Assuming StartingPage is another class where you define your starting page
        self.start = StartingPage()
        self.start.show()

class UnlabelledOptionsPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unlabelled Options")
        self.setGeometry(100, 100, 400, 200)
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.upload_button = QPushButton("Upload Images")
        self.upload_button.clicked.connect(self.open_upload_page)
        layout.addWidget(self.upload_button)

        self.label_button = QPushButton("Label Images")
        self.label_button.clicked.connect(self.label_images)  # Placeholder functionality
        layout.addWidget(self.label_button)

    def open_upload_page(self):
        self.hide()
        self.upload_page = UploadPage()
        self.upload_page.show()

    #def label_images(self):
    #   QMessageBox.information(self, "Label Images", "Label images functionality to be implemented.")
    def label_images(self):
        # Open a window to display all images from the 'all_images' database
        try:
            client = MongoClient('mongodb://localhost:27017/')
            db = client['all_images']
            self.all_images_window = AllImagesWindow(db)
            self.all_images_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
class StartingPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle("Starting Page")
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        self.label = QLabel("Do you want to see the labelled photos or Unlabelled?")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont('Arial', 20))
        main_layout.addWidget(self.label)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.b1 = QPushButton("Labelled")
        self.b1.setFont(QFont('Arial', 16))
        self.b1.clicked.connect(self.show_labelled_photos)  # Connect to show labelled photos method
        button_layout.addWidget(self.b1)

        self.b2 = QPushButton("Unlabelled")
        self.b2.setFont(QFont('Arial', 16))
        self.b2.clicked.connect(self.open_unlabelled_options)
        button_layout.addWidget(self.b2)

        main_layout.addLayout(button_layout)

    def show_labelled_photos(self):
        self.hide()
        self.labelled_photos_window = ScrollListExample(self)  # Pass the reference to the main window
        self.labelled_photos_window.show()

    def open_unlabelled_options(self):
        self.hide()
        self.unlabelled_options = UnlabelledOptionsPage()
        self.unlabelled_options.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = StartingPage()
    main_window.show()
    sys.exit(app.exec())
