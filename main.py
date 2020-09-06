import pygame
from view.view import View
from controller.controller import Controller

view = View()
controller = Controller()

times = [pygame.time.get_ticks(), pygame.time.get_ticks()]

running = True
while running:
    events_list = pygame.event.get()

    # Tymaczasowo
    for event in events_list:
        if event.type == pygame.QUIT:
            running = False

    times[0], times[1] = times[1], pygame.time.get_ticks()
    delta_time = times[1] - times[0]

    controller.get_pressed_keys(delta_time)
    view.update()
