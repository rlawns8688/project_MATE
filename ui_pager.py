from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys

# image_paths = [
#     "/home/rapa/myproject/test/script_test/frame_0001.png",
#     "/home/rapa/myproject/test/script_test/frame_0001.png",
#     "/home/rapa/myproject/test/script_test/frame_0001.png",
# ]


class ImagePager(QWidget):
    def __init__(self, image_paths):
        super().__init__()
        self.image_paths = image_paths
        self.current_page = 0
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.prev_button = QPushButton("PREV")
        self.next_button = QPushButton("NEXT")
        self.prev_button.clicked.connect(self.go_prev)
        self.next_button.clicked.connect(self.go_next)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)

        self.layout.addWidget(self.image_label)
        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

        self.update_image()

    def go_prev(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_image()

    def go_next(self):
        if self.current_page < len(self.image_paths) - 1:
            self.current_page += 1
            self.update_image()

    def update_image(self):
        pixmap = QPixmap(self.image_paths[self.current_page])
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_image()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.pager = ImagePager(image_paths)
        self.setCentralWidget(self.pager)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
