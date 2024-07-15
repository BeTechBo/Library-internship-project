from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
import pymongo
from gridfs import GridFS
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor

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
