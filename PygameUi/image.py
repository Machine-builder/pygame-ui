import pygame
from .widget import Widget

class ImageWidget(Widget):
    def __init__(self, parent=None, image:pygame.Surface=None):
        super().__init__(parent)
        self.set_image(image)
    
    def set_image(self, image):
        """set the widget's image"""
        self.image = image
        self.image_size = self.image.get_size()
        self.image_size_half = (int(self.image_size[0]/2),
                                int(self.image_size[1]/2))
        self.set_minimum_size(*self.image.get_size())
    
    def draw_after(self, surface):
        """draw the image widget"""
        center = self.center
        image_pos = (center[0]-self.image_size_half[0],
                     center[1]-self.image_size_half[1])
        surface.blit(self.image, image_pos)