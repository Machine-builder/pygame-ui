import pygame

from . import WidgetTypes
from . import Image

class Label(Image):
    """basic label

    can display text"""

    def __init__(self, parent=None, font:pygame.font.Font=None, text=''):
        self.font = font
        self.set_text(text)
        super().__init__(parent, self.image)
        self.type = WidgetTypes.LABEL
    
    def set_text(self, text):
        self.image = self.font.render(text,True,(0,0,0))