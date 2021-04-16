class Checks():
    """a few "check" functions for widgets
    
    is_focused, is_hovered"""

    @staticmethod
    def is_focused(widget):
        return widget.is_focused
    
    @staticmethod
    def is_hovered(widget):
        return widget.is_hovered

Shortnames = {
    'focused': Checks.is_focused,
    'hovered': Checks.is_hovered
}