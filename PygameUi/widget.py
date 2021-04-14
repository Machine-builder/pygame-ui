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

import copy
import math

class WidgetLayout():
    """a widget's layout values

    used for children to define whether
    they should stretch, and how much
    room they should take up"""

    def __init__(self, stretch=(True,True), stretch_value=(1,1)):
        self.stretch = stretch
        self.stretch_value = stretch_value

        self.margin = (0,0,0,0)

class WidgetStyle():
    """a widget's style
    
    controls how the widget is drawn"""

    def __init__(self, background=(200,200,200), border=(0,(0,0,0)), border_radius=5):
        self.background = background
        self.border = border
        self.border_radius = border_radius
    
    def draw(self, surface, rect):
        pygame.draw.rect(surface=surface,
                         color=self.background,
                         rect=rect,
                         border_radius=self.border_radius)
        if self.border[0] != 0:
            border_width, border_colour = self.border
            pygame.draw.rect(surface=surface,
                             color=border_colour,
                             rect=rect,
                             width=border_width,
                             border_radius=self.border_radius)

class Widget():
    """basic Widget class
    
    stores:
     - name
     - size
     - location
     - children"""
    
    def __init__(self, parent=None):
        self._parent = parent

        self._name = 'widget'
        self._size = (100,100)
        self._min_size = (5,5)
        self._loc = (0,0)

        self.fixed_min_size = (False, (0,0))

        self._padding = (2,2,2,2)

        self._wlayout = WidgetLayout()
        self._style = WidgetStyle()

        self._children = []

        self.set_layout(Layout())
        self.minimum_size = self.get_minimum_size()

        self._on_click = None

        self.type = WidgetTypes.WIDGET
    
    def copy(self):
        return copy.deepcopy(self)

    @property
    def parent(self): return self._parent
    @parent.setter
    def parent(self, parent=None):
        self._parent = parent
    
    @property
    def name(self): return self._name
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def size(self): return self._size
    @size.setter
    def size(self, size):
        self._size = (
            max(self.minimum_size[0],size[0]),
            max(self.minimum_size[1],size[1]))
        self.reposition_children()

    @property
    def loc(self): return self._loc
    @loc.setter
    def loc(self, loc):
        self._loc = loc
    
    @property
    def padding(self): return self._padding
    @padding.setter
    def padding(self, padding):
        if type(padding) == tuple:
            if len(padding) == 4:
                self._padding = padding
            elif len(padding) == 2:
                self._padding = (padding[1],
                                 padding[0],
                                 padding[1],
                                 padding[0])
        elif type(padding) == int:
            self._padding = (padding,padding,padding,padding)
        self.reposition_children()
    
    @property
    def wlayout(self): return self._wlayout
    @wlayout.setter
    def wlayout(self, wlayout):
        self._wlayout = wlayout
        if self.parent:
            self.parent.reposition_children()

    @property
    def style(self): return self._style
    @style.setter
    def style(self, style=WidgetStyle):
        self._style = style
    
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
    def x(self): return self._loc[0]
    @property
    def y(self): return self._loc[1]

    @property
    def center(self):
        rw = self.w+self.margin[1]+self.margin[3]
        rh = self.h+self.margin[0]+self.margin[2]
        return (
            int(self.scrn_x + rw/2 - self.margin[1]),
            int(self.scrn_y + rh/2 - self.margin[0])
        )

    @w.setter
    def w(self,w):
        self.size = (w,self._size[1])
    @h.setter
    def h(self,h):
        self.size = (self._size[0],h)
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
    
    def set_fluid_size(self,x=1,y=1):
        """sets how a widget should act in a parent widget
        
        x & y should both be either floats or ints,
        and x is the "weight" of this widget if it's in a row,
        and y is the "weight" of this widget if it's in a column.
        
        weights of a widget basically allow it to take up
        more space in organisation"""
        sx = bool(x)
        sy = bool(y)
        self.wlayout.stretch = (sx,sy)
        self.wlayout.stretch_value = (
            x if sx else 1,
            y if sy else 1
        )

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
    
    def ensure_positive_margin(self):
        self.wlayout.margin = (
            max(self.wlayout.margin[0],0), max(self.wlayout.margin[1],0),
            max(self.wlayout.margin[2],0), max(self.wlayout.margin[3],0)
        )
    
    @property
    def margin(self):
        return self.wlayout.margin
    @margin.setter
    def margin(self, margin):
        if type(margin) == tuple:
            if len(margin) == 4:
                self.wlayout.margin = margin
            elif len(margin) == 2:
                self.wlayout.margin = (margin[1], margin[0],
                                       margin[1], margin[0])
        elif type(margin) == int:
            self.wlayout.margin = (margin,margin,margin,margin)
        self.ensure_positive_margin()
        self.reposition_children()
    
    def set_name(self, name:str):
        self.name = name
    def set_size(self, size:tuple):
        self._size = size
        self.reposition_children()
    def set_loc(self, loc:tuple):
        self._loc = loc
    def set_style(self, style):
        self._style = style
    def set_layout(self, layout:Layout):
        """set a layout for the widget's children to follow"""
        self._layout = layout
        self.reposition_children()
    
    def draw(self, surface):
        """draw the widget onto the surface"""
        self._style.draw(surface, self.rect)
        self.ovr_draw(surface)
        for child in self._children:
            child.draw(surface)
    
    def add_child(self, child):
        """add one child to the widget's children"""
        self.add_children([child],)

    def add_children(self, children:list):
        """add a list of children to the widget's children"""
        self._children.extend(children)
        for child in children:
            child.parent = self
        self.reposition_children()
    
    def set_minimum_size(self, w, h):
        self._min_size = (w,h)
    
    def ovr_draw(self, surface):
        """function intended to be overwritten"""
    
    @property
    def on_click(self): return self._on_click
    @on_click.setter
    def on_click(self, function):
        """set a widget's on_click attribute to a function"""
        if function:
            self.type = WidgetTypes.BUTTON
        self._on_click = function
    
    def all_children(self):
        """return a list of all children (deep search)"""
        children = []
        for child in self._children:
            children.append(child)
            if len(child._children)>0:
                children.extend(child.all_children())
        return children
    
    def filter_children(self, filter_function):
        """return a list of all children that match the filter"""
        matches = filter(filter_function,
                         [child for child in self.all_children()])
        return matches

    def get_minimum_size(self, debug=False, indent=0):
        """returns the minimum size of the widget,
        taking all children widgets into account"""

        # set the min_size to the widget's padding & margin
        min_size = [
            self.min_w,
            self.min_h
        ]

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
        
        layout = self._layout

        # if this widget has children, add up their sizes
        if len(self._children) > 0:

            if layout.size == Layout.FIT:
                if layout.direction == Layout.ROW:
                    i0, i1 = 0, 1
                elif layout.direction == Layout.COL:
                    i0, i1 = 1, 0
                
                # flip the axis being calculated
                # depending on whether the child widgets
                # are on a row or column

                largest = 0
                child_sizes = []

                for child in self._children:
                    child_min_size = child.get_minimum_size(debug, indent+4)
                    if child.wlayout.stretch[i0]:
                        weight = child.wlayout.stretch_value[i0]
                        value = child_min_size[i0]/weight
                        child_sizes.append((value,weight),)
                    else:
                        min_size[i0] += child.w if i0==0 else child.h
                    largest = max(largest, child_min_size[i1])

                child_sizes.sort(key=lambda i: i[0], reverse=True)
                largest_v = child_sizes[0][0]

                for _,w in child_sizes:
                    min_size[i0] += largest_v*w

                min_size[i1] += largest
        
        return tuple(min_size)
    
    def stretch_to_max(self, children, index=0):
        return sum([child.wlayout.stretch_value[index] for child in children])
    
    def reposition_children(self):
        """reposition own children based on layout"""

        self.minimum_size = self.get_minimum_size()

        # if this widget has no children, don't do anything
        # otherwise we'll run into x/0 division errors
        if len(self._children) == 0: return

        layout = self._layout

        if layout.direction == Layout.ROW:
            if layout.size == Layout.FIT:
                # all child widgets should be even width

                # get a list of children which are allowed to stretch on the x axis
                fluid_width_children = list([child for child in self._children if child.wlayout.stretch[0]])
                # get a list of children which are not allowed to stretch on the x axis
                fixed_width_children = list([child for child in self._children if not child.wlayout.stretch[0]])
                
                # calculate the area of space which is given to stretchable children
                stretch_width = self._size[0]
                stretch_width -= sum([child.size[0] for child in fixed_width_children])
                stretch_width -= self._padding[1] # L padding (left)
                stretch_width -= self._padding[3] # R padding (right)
                stretch_width -= self.margin[1]
                stretch_width -= self.margin[3]

                # calculate the sum of all the stretch values of fluid children
                # this is useful, because some children will need to take up 2x the room
                # that another fluid child takes up - so this allows it to take up that amount
                stretch_to_max = self.stretch_to_max(fluid_width_children, 0)

                # calculate the width of each stretchable child according to the maximum area
                width_individual = stretch_width/stretch_to_max

                # calculate the individual height of each child widget
                height_individual = self.h
                height_individual -= self._padding[0] # T padding (top)
                height_individual -= self._padding[2] # B padding (bottom)
                height_individual -= self.margin[0] # T margin (top)
                height_individual -= self.margin[2] # B margin (bottom)

                # track the x position for each child widget,
                # so we can move it according to each child's width
                x_position = self._padding[1] + self.margin[1]

                # change the widths of all the fluid-width children
                for child in self._children:
                    # set the child's width to the calculated value, multiplied by its
                    # stretch_value (x) - which is it's multiplier to take up more room
                    if child in fluid_width_children:
                        widget_width = int(width_individual*child.wlayout.stretch_value[0])
                        child.w = widget_width
                    child.x = x_position
                    x_position += child.w
                
                for child in self._children:
                    child.h = height_individual
                    # set the child's y position to this widget's padding
                    # basically, push it down a bit to give it room from
                    # the top border
                    child.y = self._padding[0] + self.margin[0]
        
        elif layout.direction == Layout.COL:
            if layout.size == Layout.FIT:
                # all child widgets should be even height

                # get a list of children which are allowed to stretch on the y axis
                fluid_width_children = list([child for child in self._children if child.wlayout.stretch[1]])
                # get a list of children which are not allowed to stretch on the y axis
                fixed_width_children = list([child for child in self._children if not child.wlayout.stretch[1]])
                
                # calculate the area of space which is given to stretchable children
                stretch_height = self._size[1]
                stretch_height -= sum([child.size[1] for child in fixed_width_children])
                stretch_height -= self._padding[0] # T padding (top)
                stretch_height -= self._padding[2] # B padding (bottom)
                stretch_height -= self.margin[0]
                stretch_height -= self.margin[2]

                # calculate the sum of all the stretch values of fluid children
                # this is useful, because some children will need to take up 2x the room
                # that another fluid child takes up - so this allows it to take up that amount
                stretch_to_max = self.stretch_to_max(fluid_width_children, 1)

                # calculate the height of each stretchable child according to the maximum area
                height_individual = stretch_height/stretch_to_max

                # calculate the individual height of each child widget
                width_individual = self.w
                width_individual -= self._padding[1] # L padding (left)
                width_individual -= self._padding[3] # R padding (right)
                width_individual -= self.margin[1] # L margin (left)
                width_individual -= self.margin[3] # R margin (right)

                # track the y position for each child widget,
                # so we can move it according to each child's height
                y_position = self._padding[0] + self.margin[0]

                # change the widths of all the fluid-height children
                for child in self._children:
                    # set the child's height to the calculated value, multiplied by its
                    # stretch_value (y) - which is it's multiplier to take up more room
                    if child in fluid_width_children:
                        widget_height = int(height_individual*child.wlayout.stretch_value[1])
                        child.h = widget_height
                    child.y = y_position
                    y_position += child.h
                
                for child in self._children:
                    child.w = width_individual
                    # set the child's x position to this widget's padding
                    # basically, push it right a bit to give it room from
                    # the left border
                    child.x = self._padding[1] + self.margin[1]