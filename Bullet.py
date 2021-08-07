# -*- coding:utf-8 -*-
#Bulletクラスおよびその子クラスを記述

import pygame
from pygame.locals import Rect

from Entity import Entity
from Settings import WIDTH, HEIGHT, INFO_AREA, SURFACE

class Bullet(Entity):
    #発射される弾のクラス
    def __init__(self, x, y):
        #初期化
        super().__init__()
        self.x = x
        self.y = y
        self.width = 5 #弾の大きさ
        self.height = 5
        self.speed = 20
        self.image = None
        self.damage = 10

    def disp(self, hitbox=False):
        SURFACE.blit(self.image, (self.x, self.y))
        if hitbox:
            rect_image = Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(SURFACE, (0, 255, 0), rect_image, width=2)
        return

    def move(self):
        self.x += self.speed

    def is_over_display(self):
        return WIDTH <= self.x

class Machinegun(Bullet):
    #弾クラスを継承したマシンガンクラス
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 20
        self.height = 5
        self.width = 5
        self.damage = 10
        self.image = pygame.image.load("img/bullet.png")

class Missile(Bullet):
    #弾クラスを継承したミサイルクラス
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 0
        self.height = 6
        self.width = 15
        self.damage = 20
        self.image = pygame.image.load("img/missile.png")

    def move(self):
        self.x += self.speed
        self.speed = self.speed + 3
        return
