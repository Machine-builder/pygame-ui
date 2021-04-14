

class Layout():
    """a Layout,

    used to set a widget's child
    positions and sizes
    
    attributes:
     - direction : ROW, COL, ~GRID~
     - size : FIT, TOP, BOT
     
    size: FIT allows the children
    widgets to squash and stretch
    to fill the given space
    
    size: TOP snaps children
    widgets to the top, and orders
    them downwards
    
    size: BOT is basically the same
    as TOP, except they're snapped
    to the bottom instead"""

    ROW = 0
    COL = 1
    GRID = 2

    FIT = 0
    TOP = 1
    BOT = 2

    def __init__(self, direction=0, size=0):
        self.direction = direction
        self.size = size