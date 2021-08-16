# -*- coding:utf-8 -*-
#Bulletクラスおよびその子クラスを記述

import pygame
from pygame.locals import Rect
from math import pi, sin, cos

from Entity import Entity
from Settings import WIDTH, HEIGHT, INFO_AREA, SURFACE
from Settings import IMG_MISSILE, IMG_MACHINEGUN, IMG_SINKER_BULLET, IMG_DOWN_MISSILE

class Bullet(Entity):
    #発射される弾のクラス
    #斜めに弾を発射させるため、angleを追加
    def __init__(self, x, y, angle=0):
        #初期座標x, y 水平右向きを0度、垂直上向きを90度としたangle
        #初期化
        super().__init__()
        self.x = x
        self.y = y
        self.width = 5 #弾の大きさ
        self.height = 5
        self.speed = 20
        self.image = None
        self.damage = 10
        self.angle = angle * pi / 180 #ラジアンに変換

    def disp(self, hitbox=False):
        #Bulletインスタンスを描画する、hitbox=Trueで当たり判定を可視化する
        SURFACE.blit(self.image, (self.x, self.y))
        if hitbox:
            rect_image = Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(SURFACE, (0, 255, 0), rect_image, width=2)
        return

    def move(self):
        #弾の座標を動かす
        self.x = self.x + cos(self.angle)*self.speed
        self.y = self.y - sin(self.angle)*self.speed

    def is_over_display(self):
        #画面外に出たらTrueを返す
        r =  (self.x + self.width < 0) or (WIDTH < self.x)\
            or (self.y + self.height < 0) or (HEIGHT < self.y)
        return r

class Machinegun(Bullet):
    #弾クラスを継承したマシンガンクラス
    def __init__(self, x, y, angle=0):
        super().__init__(x, y, angle)
        self.speed = 20
        self.height = 5
        self.width = 5
        self.damage = 10
        self.image = pygame.image.load(IMG_MACHINEGUN)

class Missile(Bullet):
    #弾クラスを継承したミサイルクラス
    def __init__(self, x, y, angle=0):
        super().__init__(x, y, angle)
        self.speed = 0
        self.height = 6
        self.width = 15
        self.damage = 20
        self.image = pygame.image.load(IMG_MISSILE)

    def move(self):
        max = 30
        self.x += self.speed
        if self.speed < max:
            self.speed = self.speed + 3
        return

class DownMissile(Bullet):
    #弾クラスを継承した斜め下にすすむミサイルクラス
    def __init__(self, x, y):
        super().__init__(x, y, angle=-45)
        self.speed = 10
        self.height = 6
        self.width = 15
        self.damage = 20
        self.image = pygame.image.load(IMG_DOWN_MISSILE)

class SinkerBullet(Bullet):
    def __init__(self, x, y, angle=0):
        super().__init__(x, y, angle)
        self.speed = 5
        self.height = 10
        self.width = 10
        self.damage = 10
        self.image = pygame.image.load(IMG_SINKER_BULLET)
