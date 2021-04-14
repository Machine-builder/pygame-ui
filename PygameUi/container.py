import pygame
from . import widget

class Container(widget.Widget):
    """basic Container class

    built off Widget class"""
    
    def __init__(self):
        super().__init__()