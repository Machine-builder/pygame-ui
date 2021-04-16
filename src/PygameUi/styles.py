import pygame
from .widget_tags import Tags
from typing import Union


class Utility():
    @staticmethod
    def Colour(colour):
        """takes an argument, and returns an RGB tuplet"""
        if type(colour) == tuple:
            return colour
        if type(colour) == list:
            return tuple(colour)
        if type(colour) == int:
            return (colour,colour,colour)
        if type(colour) == float:
            return Utility.Colour(int(colour*255))
    
    @staticmethod
    def QuadTLBR(value):
        """takes an argument, and returns a TLBR tuplet"""
        if type(value) == tuple:
            if len(value) == 4:
                return value
            if len(value) == 2:
                return (value[1], value[0],
                        value[1], value[0])
        if type(value) == list:
            if len(value) == 4:
                return tuple(value)
            if len(value) == 2:
                return (value[1], value[0],
                        value[1], value[0])
        if type(value) == int:
            return (value,value,value,value)


class Style():
    """a widget's style
    
    controls how the widget is drawn,
    and how the widget acts as a child"""

    def __init__(self, background=(200,200,200), border=(0,(0,0,0)), border_radius=5):
        self._background = background
        self._border = border
        self._border_radius = border_radius

        self._transparent_background = False
        
        self.stretch = (True,True)
        self.stretch_value = (1,1)

        self._margin = (0,0,0,0)
        self._margin_align = (Tags.CENTER,Tags.CENTER)

        self._padding = (0,0,0,0)
    
    def draw(self, surface, rect):
        if not self._transparent_background:
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
        self._background = Utility.Colour(colour)
    def set_background(self, colour):
        self.background = colour
    
    @property
    def transparent_background(self):
        return self._transparent_background
    @transparent_background.setter
    def transparent_background(self, value:bool):
        self._transparent_background = value
    def set_transparent_background(self, value:bool):
        self.transparent_background = value
    
    @property
    def border(self):
        return self._border
    @border.setter
    def border(self, border):
        self._border = border
    def set_border(self, border):
        self.border = border
    
    @property
    def border_colour(self):
        return self._border[1]
    @border_colour.setter
    def border_colour(self, colour):
        self._border = (self._border[0],Utility.Colour(colour))
    def set_border_colour(self, colour):
        self.border_colour = colour
    
    @property
    def border_thickness(self):
        return self._border[0]
    @border_thickness.setter
    def border_thickness(self, thickness:int):
        self._border = (thickness, self._border[1])
    def set_border_thickness(self, thickness:int):
        self.border_thickness = thickness
    
    @property
    def border_radius(self):
        return self._border_radius
    @border_radius.setter
    def border_radius(self, radius:int):
        self._border_radius = radius
    def set_border_radius(self, radius:int):
        self.border_radius = radius
    
    @property
    def margin(self):
        return self._margin
    @margin.setter
    def margin(self, margin):
        self._margin = Utility.QuadTLBR(margin)
        self.ensure_positive_margin()
    
    def ensure_positive_margin(self):
        self._margin = (max(self._margin[0],0), max(self._margin[1],0),
                        max(self._margin[2],0), max(self._margin[3],0))
    
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
        self._padding = Utility.QuadTLBR(padding)