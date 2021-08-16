# -*- coding:utf-8 -*-
#Budクラスおよびその子クラスを記述

import pygame
from pygame.locals import Rect

from Entity import Entity
from Bullet import SinkerBullet
from Settings import WIDTH, HEIGHT, INFO_AREA, SURFACE, SCROLL_SPEED
from Settings import BUD_TYPE, FLOATER, SINKER

import math # get_angle


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
        self._mag = 0
        self.magazine = 0

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

    def get_angle(self, entity):
        #別のエンティティの中心への角度を取得する
        x = (entity.x + 0.5 * entity.width) - (self.x + 0.5 * self.width)
        y = (entity.y + 0.5 * entity.height) - (self.y + 0.5 * self.height)
        rad = math.atan2(y, x)
        deg = (180 / math.pi) * rad
        return -1 * deg

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

    def mag(self):
        return self._mag

    def shoot(self, ship):
        #自機の中心方向に向かって弾を生成するメソッド
        return

    def reload(self):
        if self.magazine < self.mag():
            self.magazine += 1

class Floater(Bud):
    #浮いてる敵キャラ
    def __init__(self, x, y):
        super().__init__(x, y)
        self.name = 'Floater'
        self.num = 1 #bud番号
        self.width = BUD_TYPE[self.num]['width']
        self.height = BUD_TYPE[self.num]['height']
        self.image = pygame.image.load(BUD_TYPE[self.num]['img'])
        self.hp = BUD_TYPE[self.num]['hp']
        self.speed = 5

    def move(self, field):
        self.y += self.speed
        if field.collision(self):
            self.speed = self.speed * (-1)
        elif self.y <= 0 or self.y+self.height >= HEIGHT:
            self.speed = self.speed * (-1)
        self.x -= SCROLL_SPEED #画面スクロールに付随して動かす

class Sinker(Bud):
    #地面にいる敵キャラ
    def __init__(self, x, y, direction):
        #direction => 'up', 'down',
        super().__init__(x, y)
        self.name = 'Sinker'
        self.num = 2 #bud番号
        self.width = BUD_TYPE[self.num]['width']
        self.height = BUD_TYPE[self.num]['height']
        self.image = pygame.image.load(BUD_TYPE[self.num]['img'][direction])
        self.hp = BUD_TYPE[self.num]['hp']
        self.speed = 0

        self._mag = BUD_TYPE[self.num]['mag'] #射撃する感覚の設定
        self.magazine = 0 #打つ間隔のための変数

    def move(self, field):
        self.x -= SCROLL_SPEED #画面スクロールに付随して動かす

    def shoot(self, ship):
        #弾のクラスを返す、shipに向かって射撃
        if self.magazine >= self.mag():
            self.magazine -= self.mag()
            angle = self.get_angle(ship)
            bul = SinkerBullet(self.x + 0.5 * self.width, self.y + 0.5 * self.height, angle)
            return bul
        return None
