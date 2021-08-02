# -*- coding:utf-8 -*-

import pygame
import sys
from pygame.locals import QUIT, Rect, KEYDOWN,  K_w, K_a, K_s, K_d, K_SPACE
from random import randint

from abc import ABCMeta, abstractmethod

class Entity(metaclass=ABCMeta):
    def __init__(self):
        #エンティティの初期化
        self.x = 0 #位置x
        self.y = 0 #位置y
        self.width = 1
        self.height = 1
        self.damage = 1
        self.hp = 127

    def get_location(self):
        #位置のリストを返す
        return [self.x, self.y]

    def get_size(self):
        #幅と高さのリストを返す
        return [self.width, self.height]

    def get_damege(self):
        return self.damage

    def get_hp(self):
        return self.hp

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def disp(self):
        pass

    def collision(self, en) -> bool:
        #他のエンティティと接触していないかどうかを調べる
        x = en.x
        y = en.y
        w = en.width
        h = en.height
        r = ((x >= self.x and x <= self.x + self.width)or\
        (x<self.x and self.x < x + w)) and \
        ((y >= self.y and y <= self.y + self.height)or\
        (y < self.y and self.y < y+h))
        return r
