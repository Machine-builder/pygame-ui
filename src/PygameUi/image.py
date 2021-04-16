import pygame
from . import WidgetTypes
from . import Widget

class Image(Widget):
    def __init__(self, parent=None, image:pygame.Surface=None):
        super().__init__(parent)
        self._image=  image
        self.set_image(image)
        self.type = WidgetTypes.IMAGE
    
    @property
    def image(self):
        return self._image
    @image.setter
    def image(self, image):
        self.set_image(image)
    
    def set_image(self, image):
        """set the widget's image"""
        self._image = image
        self.image_size = self._image.get_size()
        self.image_size_half = (int(self.image_size[0]/2),
                                int(self.image_size[1]/2))
        self.set_minimum_size(*self._image.get_size())
    
    def ovr_draw(self, surface):
        """draw the image widget"""
        center = self.center
        image_pos = (center[0]-self.image_size_half[0],
                     center[1]-self.image_size_half[1])
        surface.blit(self.image, image_pos)
        # pygame.draw.circle(surface, (100,255,100), center, 7, 2)