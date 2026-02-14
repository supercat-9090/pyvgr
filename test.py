#!/usr/bin/env python
import pygame
import vgr
print("Test started")
print("Initiating")
win = pygame.display.set_mode((640, 640))
print("Main loop starting")
running = True
test = vgr.entity()
test.showHitbox = True
test.window = win
test.coll = True
tilemap = vgr.tilemap()
tilemap.tileset = [vgr.img("empty.png",True,(64,64)),vgr.img("grass.png",False,(64,64))]
tilemap.blockSize = 64
tilemap.map = [
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,1,1,0,0,0,0],
        [0,0,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],]
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    win.fill((255,0,0))
    win.blit(tilemap.surface((0,0),(640,640)),(0,0))
    test.move([pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d],events)
    test.update(activeTileCollide = [tilemap,[1]],events=events)
    pygame.display.flip()
print("Quit")
