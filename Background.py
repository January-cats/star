# -*- coding:utf-8 -*-
#背景のクラス

import pygame
from pygame.locals import Rect
from random import randint

from Entity import Entity
from Settings import WIDTH, HEIGHT, INFO_AREA, SURFACE

class Star(Entity):
    def __init__(self):
        super().__init__()
        self.x = randint(1, WIDTH)
        self.y = randint(0, HEIGHT)
        self.xv = randint(1, 10)
        self.color = (255, 255, 255)

    def disp(self):
        rect_image = Rect(self.x, self.y, 2, 2)
        pygame.draw.rect(SURFACE, self.color, rect_image)

    def move(self):
        self.x -= self.xv
        if self.x <= 0:
            self.x = WIDTH
            self.y = randint(0, HEIGHT)
            self.xv = randint(1, 10)
