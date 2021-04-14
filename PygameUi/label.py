import pygame
from .image import ImageWidget

class Label(ImageWidget):
    def __init__(self, parent=None, font:pygame.font.Font=None, text=''):
        self.font = font
        self.set_text(text)
        super().__init__(parent, self.image)
    
    def set_text(self, text):
        self.image = self.font.render(text,True,(0,0,0))