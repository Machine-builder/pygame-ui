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

from typing import Union

from . import WidgetTypes
from . import Layout
from .widget_tags import Tags
from .styles import Style
from . import widget_checks

import copy
import math



class Widget():
    """basic Widget class
    
    stores:
     - name
     - size
     - location
     - children (used in containers)
     - style
    """
    
    def __init__(self, parent=None):
        self._parent = parent

        self.type = WidgetTypes.WIDGET

        self._name = 'widget' #  name
        self._classes = [] # classes
        self._size = (100,100) # size
        self._min_size = (5,5) # minimum size
        self._loc = (0,0) # location (relative to parent)

        # is_fixed, size, min_margin
        self._fixed_size = (False, (10,10), (1,1,1,1))
        # is_fixed, size
        self.fixed_min_size = (False, (0,0))

        self._children = []
        self._auto_reposition_children = False
        self._has_children = False

        self._style = Style()
        self._styles_other = {}
        self.layout = Layout()
        self.minimum_size = self.get_minimum_size()

        self._on_click = None

        self._is_focused = False
        self._is_focusable = False

        self._is_hovered = False
        self._is_hoverable = False
    
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
    

    # class defining ------------------------------------------------------- #

    def add_class(self, class_name):
        self._classes.append(class_name)
    def remove_class(self, class_name):
        if self.is_class(class_name):
            self._classes.remove(class_name)
    def is_class(self, class_name):
        return class_name in self._classes
    

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
        self.size = size
    
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
        self.style.padding = padding
        self.reposition_children_check()
    
    @property
    def margin(self):
        return self.style.margin
    @margin.setter
    def margin(self, margin):
        self.style.margin = margin
        self.reposition_children_check()


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
    
    def style_copy(self):
        return copy.deepcopy(self._style)
    
    def style_other_add(self, function, style):
        self._styles_other[function] = style
    
    def style_other_remove(self, function):
        if function in self._styles_other:
            self._styles_other.pop(function)
    
    def get_style_for(self, check=widget_checks.Checks.is_focused) -> Union[Style,None]:
        if type(check) == str:
            return self._styles_other.get(widget_checks.Shortnames[check],
                                          None)
        else:
            return self._styles_other.get(check,None)
    

    # drawing/rendering ---------------------------------------------------- #

    def ovr_draw(self, surface):
        """function intended to be overwritten"""
    
    def draw(self, surface):
        """draw the widget onto the surface"""
        draw_in_style = self._style
        for function, style in self._styles_other.items():
            if function(self):
                draw_in_style = style
                break
        draw_in_style.draw(surface, self.rect)
        self.ovr_draw(surface)
        for child in self._children:
            child.draw(surface)

    
    # event-linking functionality ------------------------------------------ #

    @property
    def on_click(self): return self._on_click
    @on_click.setter
    def on_click(self, function):
        """set a widget's on_click attribute to a function"""
        if function:
            self.type = WidgetTypes.BUTTON
        self._on_click = function
    
    @property
    def is_focused(self):
        return self._is_focused
    @is_focused.setter
    def is_focused(self, value):
        self._is_focused = value
    @property
    def is_focusable(self):
        return self._is_focusable
    def set_focusable(self, focusable, style_on_focus=None):
        self._is_focusable = focusable
        check = widget_checks.Checks.is_focused
        if focusable:
            added_style = style_on_focus or self.style_copy()
            self.style_other_add(check, added_style)
        else:
            self.style_other_remove(check)
    
    @property
    def is_hovered(self):
        return self._is_hovered
    @is_hovered.setter
    def is_hovered(self, value):
        self._is_hovered = value
    @property
    def is_hoverable(self):
        return self._is_hoverable
    def set_hoverable(self, hoverable, style_on_focus=None):
        self._is_hoverable = hoverable
        check = widget_checks.Checks.is_hovered
        if hoverable:
            added_style = style_on_focus or self.style_copy()
            self.style_other_add(check, added_style)
        else:
            self.style_other_remove(check)
    

    # minimum-size calculations for scaling -------------------------------- #

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
    

    # fluid margins -------------------------------------------------------- #

    def adjust_margins_to_area(self, area_x, area_y):
        """adjust a widget's margins to make it
        a set width and height within an area"""
        _, target_size, min_margin = self.fixed_size

        self.size = (area_x, area_y)

        differenceX = area_x - target_size[0]
        differenceY = area_y - target_size[1]

        style = self.style

        if style.margin_align[0] == Tags.CENTER:
            margin_L = math.floor(differenceX/2)
            margin_R = math.ceil(differenceX/2)
        elif style.margin_align[0] == Tags.LEFT:
            margin_L = min_margin[1]
            margin_R = differenceX-min_margin[1]
        elif style.margin_align[0] == Tags.RIGHT:
            margin_L = differenceX-min_margin[3]
            margin_R = min_margin[3]
        
        if style.margin_align[1] == Tags.CENTER:
            margin_T = math.floor(differenceY/2)
            margin_B = math.ceil(differenceY/2)
        elif style.margin_align[1] == Tags.TOP:
            margin_T = min_margin[0]
            margin_B = differenceY-min_margin[0]
        elif style.margin_align[1] == Tags.BOT:
            margin_T = differenceY-min_margin[2]
            margin_B = min_margin[2]
        
        self.margin = (margin_T,margin_L,
                       margin_B,margin_R)
    

    # child repositioning -------------------------------------------------- #

    def reposition_children_check(self):
        """run self.reposition_children()
        only if auto-reposition is enabled"""
        if self._auto_reposition_children:
            self.reposition_children()
    
    def reposition_children(self):
        """reposition own children based on layout
        - function indended to be overwritten"""