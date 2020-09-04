import pygame
import config
from model import model
from view import View

view = View()

running = True
while running:
    events_list = pygame.event.get()

    # TODO
    # przeslac liste eventow do kontrolera


    # Tymaczasowo
    for event in events_list:
        if event.type == pygame.QUIT:
            running = False

    view.update()
