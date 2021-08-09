# -*- coding:utf-8 -*-
#Budクラスおよびその子クラスを記述

import pygame
from pygame.locals import Rect

from Entity import Entity
from Settings import WIDTH, HEIGHT, INFO_AREA, SURFACE
from Settings import FLOATER, SINKER


class Bud(Entity):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.image = None
        self.hp = 100
        self.speed = 5
        self.hit = False

    def disp(self, hitbox=False):
        SURFACE.blit(self.image, (self.x, self.y))
        if hitbox:
            color = (255, 0, 0) if self.hit else (0, 255, 0)
            rect_image = Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(SURFACE, color, rect_image, width=1)

    def move(self, field):
        pass

    def damage(self, num):
        self.hp -= num
        return

    def is_dead(self):
        return self.hp <= 0

    def set_hit_default(self):
        #接触していない
        self.hit = False
        return

    def hit_with(self, e):
        #接触した
        self.hit = True
        return

class Floater(Bud):
    #浮いてる敵キャラ
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = FLOATER['width']
        self.height = FLOATER['height']
        self.image = pygame.image.load(FLOATER['img'])
        self.hp = FLOATER['hp']
        self.speed = 5
        self.hit = False

    def move(self, field):
        self.y += self.speed
        self.x -= 1
        if field.collision(self):
            self.speed = self.speed * (-1)
        elif self.y <= 0 or self.y+self.height >= HEIGHT:
            self.speed = self.speed * (-1)

class Sinker(Bud):
    #地面にいる敵キャラ
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = SINKER['width']
        self.height = SINKER['height']
        self.image = pygame.image.load(SINKER['img'])
        self.hp = SINKER['hp']
        self.speed = 5
        self.hit = False

    def move(self, field):
        self.x -= 1
