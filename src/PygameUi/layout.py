from .widget_tags import Tags

class Layout():
    """a Layout,

    used to set a widget's child
    positions and sizes
    
    attributes:
     - direction : ROW, COL, ~GRID~
     - size : FIT, TOP, BOT
    (all attributes of widget_tags.Tags)
     
    size: FIT allows the children
    widgets to squash and stretch
    to fill the given space
    
    size: TOP snaps children
    widgets to the top, and orders
    them downwards
    
    size: BOT is basically the same
    as TOP, except they're snapped
    to the bottom instead"""

    def __init__(self, direction=Tags.ROW, size=Tags.FIT):
        self.direction = direction
        self.size = size