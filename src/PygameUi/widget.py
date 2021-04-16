"""

Widget features:

margin support:
    how much room the widget should
    have on all sides (len-4 tuple)
    (top, left, bottom, right)

    when setting margin, you can
    provide any of the following:
        * a single int, for all sides
        * two ints, for x & y margins
        * four ints, for all sides

padding support:
    how much room should be given
    around the inside of the widget's
    borders (len-4 tuple)
    (top, left, bottom, right)

    uses the same setting function
    as the margin

"""


import pygame

from . import WidgetTypes
from . import Layout
from .widget_tags import Tags
from .styles import Style

import copy
import math



class Widget():
    """basic Widget class
    
    stores:
     - name
     - size
     - location
     - children"""
    
    def __init__(self, parent=None):
        self._parent = parent

        self.type = WidgetTypes.WIDGET

        self._name = 'widget' #  name
        self._classes = [] #  classes
        self._size = (100,100) # size
        self._min_size = (5,5) # minimum size
        self._loc = (0,0) # location (relative to parent)

        # hard-set a minimum widget size
        # otherwise it'll just be automatically
        # calculated based on children, padding, etc
        self.fixed_min_size = (False, (0,0))
        # force the widget to stay a set size
        # this means the margins will auto
        # adjust to suit the size
        # [0] is whether to fix the size,
        # [1] is the set (w,h)
        # [2] is the minimum margin
        self._fixed_size = (False, (10,10), (1,1,1,1))

        self._padding = (2,2,2,2)

        self._auto_reposition_children = False
        self._has_children = False

        self._style = Style()

        self._children = []

        self.layout = Layout()
        self.minimum_size = self.get_minimum_size()

        self._on_click = None
    
    def copy(self):
        return copy.deepcopy(self)


    # parent-linking ------------------------------------------------------- #

    @property
    def parent(self): return self._parent
    @parent.setter
    def parent(self, parent=None):
        self._parent = parent
    

    # name defining -------------------------------------------------------- #
    
    @property
    def name(self): return self._name
    @name.setter
    def name(self, name):
        self._name = name
    

    # size functions ------------------------------------------------------- #

    @property
    def size(self): return self._size
    @size.setter
    def size(self, size):
        self._size = (
            max(self.minimum_size[0],size[0]),
            max(self.minimum_size[1],size[1]))
        self.reposition_children_check()
    
    def set_size(self, size):
        self.size = size
    def set_minimum_size(self, w, h):
        self._min_size = (w,h)
    
    @property
    def w(self): return self._size[0]
    @property
    def h(self): return self._size[1]
    @property
    def width(self): return self.w
    @property
    def height(self): return self.h
    @property
    def min_w(self): return self._min_size[0]
    @property
    def min_h(self): return self._min_size[1]
    @property
    def min_width(self): return self.min_w
    @property
    def min_height(self): return self.min_h

    @property
    def min_size(self): return self._min_size
    @min_size.getter
    def min_size(self, w, h):
        self._min_size = (w,h)
    
    @w.setter
    def w(self,w):
        self.size = (w,self._size[1])
    @h.setter
    def h(self,h):
        self.size = (self._size[0],h)

    @property
    def real_w(self):
        return self.w+self.margin[1]+self.margin[3]
    @property
    def real_h(self):
        return self.h+self.margin[0]+self.margin[2]
    
    @property
    def fixed_size(self): return self._fixed_size
    def set_fixed_size(self, fixed=True, size=(5,5), min_margin=(1,1,1,1)):
        """set a widget's fixed size, useful for in fluid widgets
        when you want to keep them a constant size"""
        self._fixed_size = (fixed, size, min_margin)
    
    @property
    def fluid_size(self): return self._style.stretch_value
    @fluid_size.setter
    def fluid_size(self, stretch_value):
        self.set_fluid_size(*stretch_value)

    def set_fluid_size(self,x=1,y=1):
        """sets how a widget should act in a parent widget
        
        x & y should both be either floats or ints,
        and x is the "weight" of this widget if it's in a row,
        and y is the "weight" of this widget if it's in a column.
        
        weights of a widget basically allow it to take up
        more space in organisation"""
        sx = bool(x)
        sy = bool(y)
        self._style.stretch = (sx,sy)
        self._style.stretch_value = (x if sx else 1,
                                     y if sy else 1)
        if self.parent:
            self.parent.reposition_children_check()
    

    # position functions --------------------------------------------------- #

    @property
    def loc(self): return self._loc
    @loc.setter
    def loc(self, loc):
        self._loc = loc
    
    @property
    def position(self): return self._loc
    @position.setter
    def position(self, position):
        self._loc = position
    
    @property
    def x(self): return self._loc[0]
    @property
    def y(self): return self._loc[1]

    @x.setter
    def x(self,x):
        self.loc = (x,self._loc[1])
    @y.setter
    def y(self,y):
        self.loc = (self._loc[0],y)
    
    @property
    def scrn_x(self):
        if not self._parent: return self.x
        return self.x+self._parent.scrn_x
    @property
    def scrn_y(self):
        if not self._parent: return self.y
        return self.y+self._parent.scrn_y

    @property
    def center(self):
        return (int(self.scrn_x + self.real_w/2 - self.margin[3]),
                int(self.scrn_y + self.real_h/2 - self.margin[2]))
    

    # padding & margins ---------------------------------------------------- #

    @property
    def padding(self):
        return self.style.padding
    @padding.setter
    def padding(self, padding):
        if type(padding) == tuple:
            if len(padding) == 4:
                self.style.padding = padding
            elif len(padding) == 2:
                self.style.padding = (padding[1],
                                 padding[0],
                                 padding[1],
                                 padding[0])
        elif type(padding) == int:
            self.style.padding = (padding,padding,padding,padding)
        self.reposition_children_check()
    
    @property
    def margin(self):
        return self.style.margin
    @margin.setter
    def margin(self, margin):
        if type(margin) == tuple:
            if len(margin) == 4:
                self.style.margin = margin
            elif len(margin) == 2:
                self.style.margin = (margin[1], margin[0],
                                     margin[1], margin[0])
        elif type(margin) == int:
            self.style.margin = (margin,margin,margin,margin)
        self.ensure_positive_margin()
        self.reposition_children_check()
    
    def ensure_positive_margin(self):
        self.style.margin = (max(self.margin[0],0), max(self.margin[1],0),
                             max(self.margin[2],0), max(self.margin[3],0))


    # borders & rects ------------------------------------------------------ #

    @property
    def rect(self):
        """the rect attribute of the widget,
        in screen coordinates"""
        margin = self.margin
        return (self.scrn_x+margin[1], self.scrn_y+margin[0],
                self.w-margin[3]-margin[1], self.h-margin[2]-margin[0])
    
    @property
    def borders(self):
        mt, ml, mb, mr = self.margin
        scrn_x, scrn_y = self.scrn_x+ml, self.scrn_y+mt
        return scrn_x, scrn_y, scrn_x+self.w-ml-mr, scrn_y+self.h-mt-mb
    
    def loc_within_borders(self, loc):
        x,y,mx,my = self.borders
        lx,ly = loc
        return lx>x and lx<mx and ly>y and ly<my
    

    # layouts & styles ----------------------------------------------------- #
    
    @property
    def layout(self):
        return self._layout
    @layout.setter
    def layout(self, layout):
        self._layout = layout
        self.reposition_children_check()
    
    @property
    def layout_direction(self):
        return self._layout.direction
    @layout_direction.setter
    def layout_direction(self, direction):
        self._layout.direction = direction
        self.reposition_children_check()

    @property
    def style(self): return self._style
    @style.setter
    def style(self, style:Style):
        self._style = style
        if self.parent:
            self.parent.reposition_children_check()
    

    # drawing/rendering ---------------------------------------------------- #

    def ovr_draw(self, surface):
        """function intended to be overwritten"""
    
    def draw(self, surface):
        """draw the widget onto the surface"""
        self._style.draw(surface, self.rect)
        self.ovr_draw(surface)
        for child in self._children:
            child.draw(surface)

    


    @property
    def on_click(self): return self._on_click
    @on_click.setter
    def on_click(self, function):
        """set a widget's on_click attribute to a function"""
        if function:
            self.type = WidgetTypes.BUTTON
        self._on_click = function
    


    def ovr_add_minimum_size(self):
        """function intended to be overwritten"""
        return (0,0)

    def get_minimum_size(self, debug=False, indent=0):
        """returns the minimum size of the widget,
        taking all children widgets into account"""

        # set the min_size to the widget's padding & margin
        min_size = [self.min_w,
                    self.min_h]

        fixed_size = self.fixed_size
        if fixed_size[0]:
            size, margins = fixed_size[1], fixed_size[2]
            min_size = [size[0] + margins[1] + margins[3],
                        size[1] + margins[0] + margins[2]]
            return min_size

        if self.fixed_min_size[0]:
            return self.fixed_min_size[1]

        min_size[0] += self.padding[1]
        min_size[0] += self.padding[3]
        min_size[0] += self.margin[1]
        min_size[0] += self.margin[3]
        
        min_size[1] += self.padding[0]
        min_size[1] += self.padding[2]
        min_size[1] += self.margin[2]
        min_size[1] += self.margin[0]

        added_minimum_size = self.ovr_add_minimum_size()
        min_size[0] += added_minimum_size[0]
        min_size[1] += added_minimum_size[1]

        return tuple(min_size)
    
    def adjust_margins_to_area(self, area_x, area_y):
        """adjust a widget's margins to make it
        a set width and height within an area"""
        _, target_size, min_margin = self.fixed_size

        self.w = area_x
        differenceX = area_x - target_size[0]
        differenceY = area_y - target_size[1]

        style = self.style

        if style.margin_align[0] == Tags.CENTER:
            margin_L, margin_R = math.floor(differenceX/2), math.ceil(differenceX/2)
        elif style.margin_align[0] == Tags.LEFT:
            margin_L, margin_R = min_margin[1], differenceX-min_margin[1]
        elif style.margin_align[0] == Tags.RIGHT:
            margin_L, margin_R = differenceX-min_margin[3], min_margin[3]
        
        if style.margin_align[1] == Tags.CENTER:
            margin_T, margin_B = math.floor(differenceY/2), math.ceil(differenceY/2)
        elif style.margin_align[1] == Tags.LEFT:
            margin_T, margin_B = min_margin[0], differenceY-min_margin[0]
        elif style.margin_align[1] == Tags.RIGHT:
            margin_T, margin_B = differenceY-min_margin[2], min_margin[2]
        
        self.margin = (margin_T,
                       margin_L,
                       margin_B,
                       margin_R)
    
    def reposition_children_check(self):
        """the function run which calls self.reposition_children()
        but only if auto-reposition is enabled"""
        if self._auto_reposition_children:
            self.reposition_children()
    
    def reposition_children(self):
        """reposition own children based on layout
        - function indended to be overwritten"""