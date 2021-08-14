# -*- coding:utf-8 -*-
#Budクラスおよびその子クラスを記述

import pygame
from pygame.locals import Rect

from Entity import Entity
from Settings import WIDTH, HEIGHT, INFO_AREA, SURFACE, SCROLL_SPEED
from Settings import BUD_TYPE, FLOATER, SINKER


class Bud(Entity):
    def __init__(self, x, y):
        self.name = 'BUD'
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.image = None
        self.hp = 100
        self.speed = 5
        self.hit = False
        self.num = 0

    def __repr__(self):
        r = '{}({}, {})'.format(self.name, self.x, self.y)
        return r

    def disp(self, hitbox=False):
        #Budインスタンスを描画する、hitbox=Trueで当たり判定を可視化する
        SURFACE.blit(self.image, (self.x, self.y))
        if hitbox:
            color = (255, 0, 0) if self.hit else (0, 255, 0)
            rect_image = Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(SURFACE, color, rect_image, width=1)

    def move(self, field):
        #Budインスタンスの座標を変化させる。子クラスで実装
        pass

    def damage(self, num):
        #hp変数を増減させる
        self.hp -= num
        return

    def is_dead(self):
        #hp変数が0以下かどうかを調べる、0以下でTrueを返す
        return self.hp <= 0

    def set_hit_default(self):
        #接触していない状態にする
        self.hit = False
        return

    def hit_with(self, e):
        #接触した状態にする
        self.hit = True
        return

class Floater(Bud):
    #浮いてる敵キャラ
    def __init__(self, x, y):
        self.name = 'Floater'
        self.num = 1 #bud番号
        self.x = x
        self.y = y
        self.width = BUD_TYPE[self.num]['width']
        self.height = BUD_TYPE[self.num]['height']
        self.image = pygame.image.load(BUD_TYPE[self.num]['img'])
        self.hp = BUD_TYPE[self.num]['hp']
        self.speed = 5
        self.hit = False

    def move(self, field):
        self.y += self.speed
        if field.collision(self):
            self.speed = self.speed * (-1)
        elif self.y <= 0 or self.y+self.height >= HEIGHT:
            self.speed = self.speed * (-1)
        self.x -= SCROLL_SPEED #画面スクロールに付随して動かす

class Sinker(Bud):
    #地面にいる敵キャラ
    def __init__(self, x, y):
        self.name = 'Sinker'
        self.num = 2 #bud番号
        self.x = x
        self.y = y
        self.width = BUD_TYPE[self.num]['width']
        self.height = BUD_TYPE[self.num]['height']
        self.image = pygame.image.load(BUD_TYPE[self.num]['img'])
        self.hp = BUD_TYPE[self.num]['hp']
        self.speed = 5
        self.hit = False

    def move(self, field):
        self.x -= SCROLL_SPEED #画面スクロールに付随して動かす
