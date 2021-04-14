import pygame
from . import container

class Window(container.Container):
    def __init__(self):
        super().__init__()
    
    def process_events(self, events):
        for event in events:
            pass