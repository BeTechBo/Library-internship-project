import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and dimensions
        self.setWindowTitle("Styled PyQt6 Application")
        self.setGeometry(100, 100, 400, 300)

        # Create a label
        self.label = QLabel("Welcome to PyQt6", self)
        self.label.setGeometry(100, 50, 200, 50)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create Button 1
        self.button1 = QPushButton("Button 1", self)
        self.button1.setGeometry(50, 150, 120, 50)
        
        # Create Button 2
        self.button2 = QPushButton("Button 2", self)
        self.button2.setGeometry(230, 150, 120, 50)

        # Set the stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2e2e2e;
            }
            QPushButton {
                font-size: 16px;
                border-radius: 10px;
                padding: 10px;
                color: white;
            }
            QPushButton#Button1 {
                background-color: #D7CEB2;
            }
            QPushButton#Button1:hover {
                background-color: #d35400;
            }
            QPushButton#Button2 {
                background-color: #1abc9c;
            }
            QPushButton#Button2:hover {
                background-color: #16a085;
            }
            QLabel {
                font-size: 20px;
                color: #ffffff;
                font-family: Helvetica, Arial, sans-serif;
            }
        """)

        # Set object names for buttons to differentiate in stylesheet
        self.button1.setObjectName("Button1")
        self.button2.setObjectName("Button2")

        # Set additional palette for the application
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#2e2e2e"))
        self.setPalette(palette)

        # Set font for the entire application
        font = QFont("Helvetica", 14)
        self.setFont(font)

# Ensure the application does not crash the notebook kernel
if __name__ == "__main__":
    app = QApplication.instance() # Check if there's already a QApplication instance running
    if app is None:
        app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Set window title and dimensions
#         self.setWindowTitle("Styled PyQt6 Application")
#         self.setGeometry(100, 100, 400, 300)

#         # Create a label
#         self.label = QLabel("Welcome to PyQt6", self)
#         self.label.setGeometry(100, 50, 200, 50)
#         self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
#         # Create Button 1
#         self.button1 = QPushButton("Button 1", self)
#         self.button1.setGeometry(50, 150, 120, 50)
        
#         # Create Button 2
#         self.button2 = QPushButton("Button 2", self)
#         self.button2.setGeometry(230, 150, 120, 50)

#         # Set the stylesheet
#         self.setStyleSheet("""
#             QMainWindow {
#                 background-color: #f0f0f0;
#             }
#             QPushButton {
#                 font-size: 16px;
#                 border-radius: 10px;
#                 padding: 10px;
#                 color: white;
#             }
#             QPushButton#Button1 {
#                 background-color: #3498db;
#             }
#             QPushButton#Button1:hover {
#                 background-color: #2980b9;
#             }
#             QPushButton#Button2 {
#                 background-color: #2ecc71;
#             }
#             QPushButton#Button2:hover {
#                 background-color: #27ae60;
#             }
#             QLabel {
#                 font-size: 20px;
#                 color: #2c3e50;
#                 font-family: Arial, Helvetica, sans-serif;
#             }
#         """)

#         # Set object names for buttons to differentiate in stylesheet
#         self.button1.setObjectName("Button1")
#         self.button2.setObjectName("Button2")

#         # Set additional palette for the application
#         palette = self.palette()
#         palette.setColor(QPalette.ColorRole.Window, QColor("#f0f0f0"))
#         self.setPalette(palette)

#         # Set font for the entire application
#         font = QFont("Arial", 12)
#         self.setFont(font)

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Set window title and dimensions
#         self.setWindowTitle("Styled PyQt6 Application")
#         self.setGeometry(100, 100, 400, 300)

#         # Create a label
#         self.label = QLabel("Welcome to PyQt6", self)
#         self.label.setGeometry(100, 50, 200, 50)
#         self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
#         # Create Button 1
#         self.button1 = QPushButton("Button 1", self)
#         self.button1.setGeometry(50, 150, 120, 50)
        
#         # Create Button 2
#         self.button2 = QPushButton("Button 2", self)
#         self.button2.setGeometry(230, 150, 120, 50)

#         # Set the stylesheet
#         self.setStyleSheet("""
#             QMainWindow {
#                 background-color: #add8e6;
#             }
#             QPushButton {
#                 font-size: 16px;
#                 border-radius: 10px;
#                 padding: 10px;
#                 color: white;
#             }
#             QPushButton#Button1 {
#                 background-color: #90ee90;
#                 color: #2c3e50;
#             }
#             QPushButton#Button1:hover {
#                 background-color: #77dd77;
#             }
#             QPushButton#Button2 {
#                 background-color: #90ee90;
#                 color: #2c3e50;
#             }
#             QPushButton#Button2:hover {
#                 background-color: #77dd77;
#             }
#             QLabel {
#                 font-size: 20px;
#                 color: #2c3e50;
#                 font-family: Helvetica, Arial, sans-serif;
#             }
#         """)

#         # Set object names for buttons to differentiate in stylesheet
#         self.button1.setObjectName("Button1")
#         self.button2.setObjectName("Button2")

#         # Set additional palette for the application
#         palette = self.palette()
#         palette.setColor(QPalette.ColorRole.Window, QColor("#add8e6"))
#         self.setPalette(palette)

#         # Set font for the entire application
#         font = QFont("Arial", 14)
#         self.setFont(font)