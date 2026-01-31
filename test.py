#!/usr/bin/env python
import pygame
import vgr
print("Test started")
print("Initiating")
win = pygame.display.set_mode((640, 640))
print("Main loop starting")
running = True
test = vgr.entity()
vgr.window = win
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    win.fill((255,0,0))
    test.update()
    pygame.display.flip()
print("Quit")
