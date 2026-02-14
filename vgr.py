#!/usr/bin/env python3
import pygame

# from math import ceil
from os import sep

pygame.init()
pygame.display.init()
window = pygame.display.set_mode((640, 640))


# functions----------------------------------------------------------------------------------------
class Tilemap:
    def __init__(self,blockSize = None):
        self.size = [0, 0]
        self.map = []
        if blockSize == None:
            self.blockSize = 32
            print("Warning, block size not defined, defaulting to 32px")
        else:
            self.blockSize = blockSize
        self.tileset = []

    def loadstr(self, string):
        string = string.split("\n")  # splits the Y axis
        for i in string:  # splits X axis
            if i == "":
                del string[string.index(i)]
            else:
                string[string.index(i)] = string[string.index(i)].split()
        self.size = [len(string[0]), len(string)]

        for i in range(self.size[1]):

            for j in range(self.size[0]):
                string[i][j] = int(string[i][j])
        self.map = string
    """
    def blit(self, window, camera):
        blockDisplayPosition = [0 - camera.pos[0], 0 - camera.pos[1]]
        currentBlockPos = [0, 0]
        winx, winy = window.get_size()
        blockIndex = 0
        tileStartPos = [
            round(camera[0] // self.blockSize),
            round(camera[1] // self.blockSize),
        ]

        for i in range(tileStartPos[1], len(self.map)):  # Draws the tile one by one
            if blockDisplayPosition[1] > winy:
                break
            for j in range(tileStartPos[0], len(self.map[i])):
                blockDisplayPosition = [
                    0 - camera[0] + j * self.blockSize,
                    0 - camera[1] + i * self.blockSize,
                ]
                if blockDisplayPosition[0] > winx:
                    break
                try:
                    window.blit(self.tileset[(self.map[i][j])], blockDisplayPosition)
                    if showdebug:
                        window.blit(
                            smallfont.render(
                                str(i) + " " + str(j), False, (0, 0, 0), (255, 255, 255)
                            ),
                            (blockDisplayPosition[0], blockDisplayPosition[1]),
                        )
                        pygame.draw.rect(
                            window,
                            (255, 255, 255),
                            (blockDisplayPosition, (self.blockSize, self.blockSize)),
                            1,
                        )
                    blockIndex += 1
                except:
                    pass
                    window.blit(errortile, blockDisplayPosition)
                currentBlockPos[0] += 1
            currentBlockPos[0] = 0
            currentBlockPos[1] += 1
    """
    def surface(self, camera, size):
        surface = pygame.Surface(size, pygame.SRCALPHA)
        blockDisplayPosition = [0 - camera[0], 0 - camera[1]]
        currentBlockPos = [0, 0]
        winx, winy = surface.get_size()
        blockIndex = 0
        tileStartPos = [
            round(camera[0] // self.blockSize),
            round(camera[1] // self.blockSize),
        ]
        for i in range(len(tileStartPos)):
            if tileStartPos[i] < 0:
                tileStartPos[i] = 0

        for i in range(tileStartPos[1], len(self.map)):  # Draws the tile one by one
            if blockDisplayPosition[1] > winy:
                break
            for j in range(tileStartPos[0], len(self.map[i])):
                blockDisplayPosition = [
                    0 - camera[0] + j * self.blockSize,
                    0 - camera[1] + i * self.blockSize,
                ]
                if blockDisplayPosition[0] > winx:
                    break
                try:
                    if self.map[i][j] != 0:
                        surface.blit(
                            self.tileset[(self.map[i][j])], blockDisplayPosition
                        )
                    if showdebug:
                        surface.blit(
                            smallfont.render(
                                str(i) + " " + str(j), False, (0, 0, 0), (255, 255, 255)
                            ),
                            (blockDisplayPosition[0], blockDisplayPosition[1]),
                        )
                        pygame.draw.rect(
                            surface,
                            (255, 255, 255),
                            (blockDisplayPosition, (self.blockSize, self.blockSize)),
                            1,
                        )
                    blockIndex += 1
                except:
                    pass
                    # surface.blit(errortile,blockDisplayPosition)

                currentBlockPos[0] += 1
            currentBlockPos[0] = 0
            currentBlockPos[1] += 1
        return surface.convert_alpha()

    def size(self):
        return [len(self.map[0]), len(self.map)]

    def convertToStr(self):
        savetxt = ""
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                savetxt = savetxt + str(self.map[i][j]) + " "
            savetxt += "\n"
        return savetxt

    def collidepoint(self, camera, point):
        relPos = [point[0] + camera[0], point[1] + camera[1]]
        relPos = [relPos[0] // self.blockSize, relPos[1] // self.blockSize]
        return relPos

    def blockAt(self, pos):
        return self.map[pos[1]][pos[0]]


class Entity:
    """
    The entity class----
    Functions:
        update()
            Updates the entity, run every frame

    """

    def __init__(
        self,
        entityType="default",
        pos=[0, 0],
        v=[0, 0],
        f=[2, 2],
        a=[0, 0],
        rot=0,
        controls=[],
        speed=4,
        image=None,
        jump=True,
        coyote=4,
        maxcoyote=6,
        jumpheight=60,
        coll=True,
        hitbox=[0, 0, 64, 64],
        showHitbox=False,
        rect=[(0, 0, 255), 0],
        g=[0, 0],
    #    oldpos=[0, 0],
    #    roundpos=True,
    #    voiddeath=False,
    #    spawnpoint=[0, 0],
    #    flip=True,
    ):
        self.pos = pos
        self.entityType = entityType
        self.v = v
        self.f = f
        self.a = a
        self.rot = rot
        self.controls = controls
        self.image = image
        self.imageright = image
        if image != None:
            self.imageleft = pygame.transform.flip(image, True, False)
        else:
            self.imageleft = None
        self.speed = speed
        self.jump = jump
        self.coyote = coyote
        self.jumpheight = jumpheight
        self.hitbox = hitbox
        self.showHitbox = showHitbox
        self.rect = rect
        self.g = g
        self.oldpos = [0,0]
        self.maxcoyote = maxcoyote
        self.roundpos = [0,0]
        self.voideath = False
        self.spawnpoint = [0,0]
        self.helddownkeys = []
        self.moveDir = [0, 0]
        self.faceright = False
        self.flip = False
        self.right = True
        self.coll = coll
        self.window = None
        self.camera = [0, 0]

    def windowSize(self, size):
        self.window = pygame.surface(size)

    def blockcolltrue(self, blockList, tilemap):
        try:
            hitpoints = [
                self.pos,
                [self.pos[0] + self.hitbox[2], self.pos[1]],
                [self.pos[0], self.pos[1] + self.hitbox[3]],
                [self.pos[0] + self.hitbox[2], self.pos[1] + self.hitbox[3]],
            ]
            for collblock in blockList:
                for i in hitpoints:
                    if (
                        collblock
                        == tilemap.map[int(i[1] // tilemap.blockSize)][
                            int(i[0] // tilemap.blockSize)
                        ]
                    ):
                        return True
        except IndexError:
            return False
        return False

    def update(self, activeTileCollide=[None, []], events=None):
        self.oldpos = self.pos
        self.v = [
            self.a[0] + self.v[0],
            self.a[1] + self.v[1],
        ]  # updates velocity using accelaration
        self.v = [
            self.g[0] + self.v[0],
            self.g[1] + self.v[1],
        ]  # updates velocity using gravity
        self.v = [
            self.v[0] / self.f[0],
            self.v[1] / self.f[1],
        ]  # updates velocity using friction
        self.pos[0] += self.v[0]  # updates postion based on velocity
        if activeTileCollide[0] is not None:
            if (
                self.blockcolltrue(activeTileCollide[1], activeTileCollide[0])
                and self.coll
            ):
                self.pos[0] -= self.v[0]
                self.v[0] = 0
        self.pos[1] += self.v[1]
        if activeTileCollide[0] != None:
            if (
                self.blockcolltrue(activeTileCollide[1], activeTileCollide[0])
                and self.coll
            ):
                self.pos[1] -= self.v[1]
                if self.jump and self.v[1] > 0:
                    self.coyote = self.maxcoyote
                self.v[1] = 0
            if self.v[1] > 0:
                if self.coyote > 0:
                    self.coyote -= 1

        self.hitbox = [self.pos[0], self.pos[1], self.hitbox[2], self.hitbox[3]]
        if self.roundpos:
            self.pos = [round(self.pos[0]), round(self.pos[1])]
        if self.window != None:
            if self.showHitbox:
                    pygame.draw.rect( self.window, self.rect[0], [
                            self.hitbox[0] - self.camera[0],
                            self.hitbox[1] - self.camera[1],
                            self.hitbox[2],
                            self.hitbox[3], ],
                        self.rect[1],
                    )
        if ( self.pos[0] > self.camera[0]
            and self.pos[1] > self.camera[1]
            and self.pos[0] < (self.camera[0] + self.window.get_size()[0])
            and self.pos[0] < (self.camera[0] + self.window.get_size()[0])
        ) and self.image !=None:
            self.window.blit(
                self.image, (self.pos[0] - self.camera[0], self.pos[1] - self.camera[1])
            )
        if len(self.controls) > 7:
            self.doublewasd = True
        else:
            self.doublewasd = False

    def move(self, controls, events, jump=False):
        controlmatch = [[1, -1], [0, -1], [1, 1], [0, 1]]
        for event in events:
            if event.type == pygame.KEYDOWN:
                for key in range(len(controls)):
                    if event.key == controls[key]:
                        if jump and controls.index(key) == 2 and self.coyote > 0:
                            self.v[1] = -self.jumpheight
                        else:
                            self.moveDir[controlmatch[key][0]] = controlmatch[key][1]
            if event.type == pygame.KEYUP:
                for key in range(len(controls)):
                    if event.key == controls[key]:
                        self.moveDir[controlmatch[key][0]] = 0
        self.a = [self.moveDir[0] * self.speed, self.moveDir[1] * self.speed]
    def respawn(self):
        self.pos = self.spawnpoint
del window

def img(source, trans=False, scale=None):
    if scale is None:
        if trans:
            img = pygame.image.load(source).convert_alpha()
        else:
            img = pygame.image.load(source).convert()
        return img
    else:
        if trans:
            img = pygame.transform.scale( pygame.image.load(source).convert_alpha(), scale)
        else:
            img = pygame.transform.scale(pygame.image.load(source).convert(), scale)
        return img

def scale(img, scale):
    img = pygame.transform.scale(img, scale)
    return img


