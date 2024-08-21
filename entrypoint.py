# This Python file uses encoding: utf-8

import sys

from PyQt5.QtWidgets import QApplication

from linking.linking import link_view_to_model
from model.main_model import MainModel
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_model = MainModel()
    link_view_to_model(main_window, main_model)
    app.exec()


if __name__ == '__main__':
    main()
