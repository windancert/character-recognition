# This Python file uses encoding: utf-8

from linking.link_image_part import link_image_part
from linking.link_text_part import link_text_part
from model.main_model import MainModel
from ui.main_window import MainWindow


def link_view_to_model(windows: MainWindow, model: MainModel):
    link_image_part(windows, model)
    link_text_part(windows, model)
