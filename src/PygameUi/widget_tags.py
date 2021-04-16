class Tags:
    """tags are basically references for numbers
    that represent different things. It's easier
    than remembering what each different number
    corresponds to
    
    available tags:
    - ROW
    - COL
    - GRID
    
    - FIT
    - TOP
    - BOT
    
    - LEFT
    - CENTER
    - RIGHT
    
    - X
    - Y"""

    ROW = 0
    COL = 1
    GRID = 2

    FIT = 0
    TOP = 1
    BOT = 2

    # used for alignment of fluid margins
    LEFT = 0
    CENTER = 1
    RIGHT = 2

    # used for buttons
    TEXT = 0
    IMAGE = 1
    BLANK = 2

    # used for axis calculations
    X = 0
    Y = 1