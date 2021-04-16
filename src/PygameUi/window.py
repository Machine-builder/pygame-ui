import pygame
from . import container

class Window(container.Container):
    def __init__(self):
        super().__init__()
    
    def process_events(self, pygame_events):
        """processes pygame events, like mouse clicks if needed"""
        mouse_position = pygame.mouse.get_pos()

        # set the is_hovered attribute for hoverable child widgets
        hoverable_children = list(self.filter_children(lambda child: child.is_hoverable))
        hovered_children = list(filter(
            lambda child: child.loc_within_borders(mouse_position),
            hoverable_children))
        for child in hoverable_children:
            child.is_hovered = child in hovered_children

        clicks = []
        for event in pygame_events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # LMB clicked and released
                    clicks.append(1)
        
        if len(clicks)>0:
            clickable_widgets = self.filter_children(
                lambda child: child.on_click)
            if 1 in clicks:
                # LMB was clicked
                # for each clickable widget, check
                # if the mouse position is over it
                for widget in clickable_widgets:
                    if widget.loc_within_borders(mouse_position):
                        widget.on_click()