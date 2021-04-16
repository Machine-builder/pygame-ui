import pygame
from . import widget
from . import WidgetTypes
from . import Layout
from .widget_tags import Tags

import math

class Container(widget.Widget):
    """basic Container class

    built off Widget class"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.type = WidgetTypes.CONTAINER
        self._has_children = True
    

    # auto-child-repositioning settings ------------------------------------ #
    
    @property
    def auto_reposition_children(self):
        return self._auto_reposition_children
    @auto_reposition_children.setter
    def auto_reposition_children(self, value):
        self._auto_reposition_children = value
    

    # child adding --------------------------------------------------------- #

    def add_child(self, child):
        """add one child to the widget's children"""
        self.add_children([child],)

    def add_children(self, children:list):
        """add a list of children to the widget's children"""
        self._children.extend(children)
        for child in children:
            child.parent = self
        self.reposition_children()

    
    # child removing ------------------------------------------------------- #

    def remove_child(self, child):
        """remove child from the widget's children
        
        returns True/False depending on whether the child
        was in the widget's children list"""
        if not child in self._children:
            return False
        self._children.remove(child)
        child.parent = None
        return True
    
    def remove_children(self, children):
        """remove a list of children from the widget's children"""
        for child in children:
            self.remove_child(child)
    

    # child getting/filtering and deep searching --------------------------- #

    def child_at(self, index):
        """get a child at an index"""
        return self._children[index]
    
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
    
    def filter_children_top(self, filter_function):
        """returns a list of all children of this widget that
        match the provided filter"""
        matches = [
            child for child in self._children if filter_function(child)]
        return matches
    

    # run functions on children -------------------------------------------- #

    def run_functions_on_children(self, function, all_children=True):
        """run a given function on this widget's children
        all_children specifies whether to run the function
        for every child under this widget (deep search),
        or just to run it for each top-level child
        
        returns the amount of children that the function
        was run on"""
        if all_children:
            run_function_on = self.all_children()
        else:
            run_function_on = self._children
        for child in run_function_on:
            function(child)
        return len(run_function_on)
    

    # minimum size check --------------------------------------------------- #
    
    def ovr_add_minimum_size(self):
        layout = self.layout
        min_size = [0,0]

        # if this widget has children, add up their sizes
        if len(self._children) > 0:

            if layout.size == Tags.FIT:
                if layout.direction == Tags.ROW:
                    i0, i1 = 0, 1
                elif layout.direction == Tags.COL:
                    i0, i1 = 1, 0
                
                # flip the axis being calculated
                # depending on whether the child widgets
                # are on a row or column

                largest = 0
                largest2 = 0
                child_sizes = []

                for child in self._children:
                    child_min_size = child.get_minimum_size()
                    if child.style.stretch[i0]:
                        weight = child.style.stretch_value[i0]
                        value = child_min_size[i0]/weight
                        child_sizes.append((value,weight),)
                    else:
                        min_size[i0] += (child.w if i0==0 else child.h)
                    largest = max(largest, child_min_size[i1])
                    largest2 = max(largest2, child_min_size[i0])

                child_sizes.sort(key=lambda i: i[0], reverse=True)

                if len(child_sizes) > 0:
                    largest_v = child_sizes[0][0]
                    for _,w in child_sizes:
                        min_size[i0] += largest_v*w
                
                else:
                    min_size[i0] += largest2

                min_size[i1] += largest
        
        return min_size
    

    # fluid area calculations ---------------------------------------------- #

    def stretch_to_max(self, children, axis=Tags.X):
        """return the maximum stretch value (the sum of
        all child widget's stretch value in a given
        axis"""
        return sum([child.style.stretch_value[axis] for child in children])
    
    def get_fluid_area(self, axis=Tags.X):
        if axis == Tags.X:
            cover_area = self.w
            cover_area -= sum([child.w for child in self.filter_children_top(
                lambda c: not c.style.stretch[0])])
            cover_area -= self.style.padding[1]
            cover_area -= self.style.padding[3]
            cover_area -= self.style.margin[1]
            cover_area -= self.style.margin[3]
            if self.name == 'debug':
                print(self.size)
                print("fluid area X:", cover_area)
        elif axis == Tags.Y:
            cover_area = self.h
            cover_area -= sum([child.h for child in self.filter_children_top(
                lambda c: not c.style.stretch[1])])
            cover_area -= self.style.padding[0]
            cover_area -= self.style.padding[2]
            cover_area -= self.style.margin[0]
            cover_area -= self.style.margin[2]
        return cover_area
    
    def align_fluid_children(self):
        """automatically adjust child widget's
        fluid values depending on their minimum
        sizes in relation to each other"""
        # get fluid area depending on whether this
        # widget is aligned as ROW or COL
        layout = self.layout
        if layout.direction == Tags.ROW:
            # calculate how much space is available
            # for fluid widgets to use up
            fluid_area = self.get_fluid_area(Tags.X)
            # get a list of all children which are fluid
            # in this axis
            fluid_children = self.filter_children_top(
                lambda c: c.style.stretch[0])
            # iterate through all the fluid children,
            # and work out their ratio for space that
            # they should take up
            for child in fluid_children:
                min_w = child.get_minimum_size()[0]
                ratio = min_w/fluid_area
                child.fluid_size = (ratio, child.fluid_size[1])
        elif layout.direction == Tags.COL:
            # calculate how much space is available
            # for fluid widgets to use up
            fluid_area = self.get_fluid_area(Tags.Y)
            # get a list of all children which are fluid
            # in this axis
            fluid_children = self.filter_children_top(
                lambda c: c.style.stretch[1])
            # iterate through all the fluid children,
            # and work out their ratio for space that
            # they should take up
            for child in fluid_children:
                min_h = child.get_minimum_size()[1]
                ratio = min_h/fluid_area
                child.fluid_size = (child.fluid_size[0], ratio)
    
    def reposition_children(self):
        """reposition own children based on layout"""

        self.minimum_size = self.get_minimum_size()

        # if this widget has no children, don't do anything
        # otherwise we'll run into x/0 division errors
        if len(self._children) == 0: return

        layout = self.layout

        if layout.direction == Tags.ROW:
            if layout.size == Tags.FIT:
                # all child widgets should be even width

                # get a list of children which are allowed to stretch on the x axis
                fluid_width_children = self.filter_children_top(lambda c: c.style.stretch[0])
                
                # calculate the area of space which is given to stretchable children
                stretch_width = self.get_fluid_area(Tags.X)

                # calculate the sum of all the stretch values of fluid children
                # this is useful, because some children will need to take up 2x the room
                # that another fluid child takes up - so this allows it to take up that amount
                stretch_to_max = self.stretch_to_max(fluid_width_children, Tags.X)

                # calculate the width of each stretchable child according to the maximum area
                width_individual = 1
                if stretch_to_max > 0:
                    width_individual = stretch_width/stretch_to_max

                # calculate the individual height of each child widget
                height_individual = self.h
                height_individual -= self.style.padding[0] # T padding (top)
                height_individual -= self.style.padding[2] # B padding (bottom)
                height_individual -= self.style.margin[0] # T margin (top)
                height_individual -= self.style.margin[2] # B margin (bottom)

                # track the x position for each child widget,
                # so we can move it according to each child's width
                x_position = self.style.padding[1] + self.style.margin[1]

                # change the widths of all the fluid-width children
                for child in self._children:
                    # set the child's width to the calculated value, multiplied by its
                    # stretch_value (x) - which is it's multiplier to take up more room

                    widget_width = child.w
                    if child in fluid_width_children:
                        widget_width = width_individual*child.style.stretch_value[0]

                        if not child.fixed_size[0]:
                            child.w = int(widget_width)
                        else:
                            available_space = int(widget_width)
                            child.adjust_margins_to_area(available_space, height_individual)

                    child.x = x_position
                    x_position += widget_width
                
                for child in self._children:
                    child.h = height_individual
                    if child.fixed_size[0]:
                        child.adjust_margins_to_area(child.w, height_individual)
                    # set the child's y position to this widget's padding
                    # basically, push it down a bit to give it room from
                    # the top border
                    child.y = self.style.padding[0] + self.style.margin[0]
        
        elif layout.direction == Tags.COL:
            if layout.size == Tags.FIT:
                # all child widgets should be even height

                # get a list of children which are allowed to stretch on the y axis
                fluid_height_children = self.filter_children_top(lambda c: c.style.stretch[1])
                
                # calculate the area of space which is given to stretchable children
                stretch_height = self.get_fluid_area(Tags.Y)

                # calculate the sum of all the stretch values of fluid children
                # this is useful, because some children will need to take up 2x the room
                # that another fluid child takes up - so this allows it to take up that amount
                stretch_to_max = self.stretch_to_max(fluid_height_children, Tags.Y)

                # calculate the height of each stretchable child according to the maximum area
                height_individual = 1
                if stretch_to_max > 0:
                    height_individual = stretch_height/stretch_to_max

                # calculate the individual width of each child widget
                width_individual = self.w
                width_individual -= self.style.padding[1] # L padding (left)
                width_individual -= self.style.padding[3] # R padding (right)
                width_individual -= self.style.margin[1] # L margin (left)
                width_individual -= self.style.margin[3] # R margin (right)

                # track the y position for each child widget,
                # so we can move it according to each child's height
                y_position = self.style.padding[0] + self.style.margin[0]

                # change the widths of all the fluid-height children
                for child in self._children:
                    # set the child's height to the calculated value, multiplied by its
                    # stretch_value (y) - which is it's multiplier to take up more room

                    widget_height = child.h
                    if child in fluid_height_children:
                        widget_height = height_individual*child.style.stretch_value[1]
                        
                        if not child.fixed_size[0]:
                            child.h = int(widget_height)
                        else:
                            available_space = int(widget_height)
                            child.adjust_margins_to_area(width_individual, available_space)
                    
                    child.y = y_position
                    y_position += widget_height
                
                for child in self._children:
                    child.w = width_individual
                    if child.fixed_size[0]:
                        child.adjust_margins_to_area(width_individual, child.h)
                    # set the child's x position to this widget's padding
                    # basically, push it right a bit to give it room from
                    # the left border
                    child.x = self.style.padding[1] + self.style.margin[1]

        for child in self._children:
            if child._has_children:
                child.reposition_children()