from . import Widget
from . import Container
from .widget_tags import Tags

class Grid(Container):
    def __init__(self, parent=None, grid_x=3, grid_y=3):
        super().__init__(parent)
        self.grid_x, self.grid_y = grid_x, grid_y
        
        for y in range(self.grid_y):
            container_row = Container(self)
            container_row.style.margin = 0
            container_row.padding = 0
            container_row.layout_direction = Tags.COL
            for x in range(self.grid_x):
                grid_item = Widget(container_row)
                grid_item.padding = 2
                grid_item.margin = 0
                grid_item.style.border_thickness = 1
                grid_item.style._border_radius = 0
                container_row.add_child(grid_item)
            self.add_child(container_row)

from typing import Union

class Foo():
    def __init__(self, size=(10,10)):
        self._size = size
    
    @property
    def size(self) -> tuple:
        return self._size
    
    @size.setter
    def size(self, new_size:Union[tuple,list,int,float]) -> None:
        if type(new_size)==tuple or type(new_size)==list:
            self._size = (new_size[0], new_size[1])
        else:
            self._size = (new_size, new_size)

abc = Foo()

abc.size = 3
# is the same as
abc.size = (3,3)