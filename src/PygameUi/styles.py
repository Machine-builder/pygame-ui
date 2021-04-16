import pygame
from .widget_tags import Tags

class Style():
    """a widget's style
    
    controls how the widget is drawn,
    and how the widget acts as a child"""

    def __init__(self, background=(200,200,200), border=(0,(0,0,0)), border_radius=5):
        self._background = background
        self._border = border
        self._border_radius = border_radius
        
        self.stretch = (True,True)
        self.stretch_value = (1,1)

        self._margin = (0,0,0,0)
        self._margin_align = (Tags.CENTER,Tags.CENTER)

        self._padding = (1,1,1,1)
    
    def draw(self, surface, rect):
        pygame.draw.rect(surface=surface,
                         color=self._background,
                         rect=rect,
                         border_radius=self._border_radius)
        if self.border[0] != 0:
            border_width, border_colour = self._border
            pygame.draw.rect(surface=surface,
                             color=border_colour,
                             rect=rect,
                             width=border_width,
                             border_radius=self._border_radius)
    
    @property
    def background(self):
        return self._background
    @background.setter
    def background(self, colour):
        self._background = colour
    
    @property
    def border(self):
        return self._border
    @border.setter
    def border(self, border):
        self._border = border
    
    @property
    def border_colour(self):
        return self._border[1]
    @border_colour.setter
    def border_colour(self, colour):
        self._border = (self._border[0], colour)
    
    @property
    def border_thickness(self):
        return self._border[0]
    @border_thickness.setter
    def border_thickness(self, thickness):
        self._border = (thickness, self._border[1])
    
    @property
    def border_radius(self):
        return self._border_radius
    @border_radius.setter
    def border_radius(self, radius):
        self._border_radius = radius
    
    @property
    def margin(self):
        return self._margin
    @margin.setter
    def margin(self, margin):
        self._margin = margin
    
    @property
    def margin_align(self):
        return self._margin_align
    @margin_align.setter
    def margin_align(self, margin_align):
        self._margin_align = margin_align
    
    @property
    def padding(self):
        return self._padding
    @padding.setter
    def padding(self, padding):
        self._padding = padding