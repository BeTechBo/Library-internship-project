import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt6.QtCore import Qt

class ScrollListExample(QWidget):
    def __init__(self):
        super().__init__()

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

        # Sample data
        people = [
            {'name': 'Mohammad Alashkar', 'image': 'C:/Users/A U C/Downloads/image1.png'},
            {'name': 'Andrew Aziz', 'image': 'C:/Users/A U C/Downloads/image2.png'},
            {'name': 'Omar Ashraf', 'image': 'C:/Users/A U C/Downloads/image3.png'},
        ]

        for person in people:
            item = QListWidgetItem()
            widget = QWidget()
            h_layout = QHBoxLayout()

            label_name = QLabel(person['name'])
            label_name.setFont(QFont('Arial', 14))
            label_image = QLabel()

            pixmap = QPixmap()
            if pixmap.load(person['image']):
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
        back_button.clicked.connect(self.close)  # Closes the window when "Back" is clicked
        back_button.setStyleSheet("QPushButton { margin: 10px; }")
        layout.addWidget(back_button)

        self.setLayout(layout)

    def on_search_button_clicked(self):
        # Placeholder for search button functionality
        print("Search button clicked")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScrollListExample()
    window.show()
    sys.exit(app.exec())
