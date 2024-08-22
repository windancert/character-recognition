# This Python file uses encoding: utf-8
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton, QFileDialog, QLabel

from linking.find_child import find_child
from model.main_model import MainModel
from ui.main_window import MainWindow


def link_image_part(window: MainWindow, model: MainModel):
    load_button: QPushButton = find_child(window, QPushButton, "image_load_pushbutton")
    load_button.clicked.connect(lambda: handle_load_button(window, model))

    model.image_model.image_changed.connect(lambda: update_image(window, model))


def handle_load_button(window: MainWindow, model: MainModel):
    path = QFileDialog.getOpenFileName(parent=window, caption="Open image file",
                                       filter='JPEG image (*.jpg);;PNG image (*.png);;All files (*.*')

    if path:
        model.image_model.load_image(path[0])


def update_image(window: MainWindow, model: MainModel):
    image_label: QLabel = find_child(window, QLabel, "picture_label")
    image = model.image_model.get_image_to_show()
    if not image:
        return
    pixmap = QPixmap.fromImage(image)
    image_label.setPixmap(pixmap)

