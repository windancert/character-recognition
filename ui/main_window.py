# This Python file uses encoding: utf-8

from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        directory_for_ui_file = Path(__file__).resolve().parent
        uic.loadUi(directory_for_ui_file.joinpath('main_window.ui'), self)
        self.show()
