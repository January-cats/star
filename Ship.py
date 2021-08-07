# -*- coding:utf-8 -*-
#Shipクラスおよびその子クラスを記述

import pygame
from pygame.locals import Rect
import copy

from Entity import Entity
from Bullet import Machinegun, Missile
from Settings import WIDTH, HEIGHT, INFO_AREA, SURFACE

class Ship(Entity):
    _mag = [
        5, # machinegun
        15, # missile
    ]
    #武器ナンバ
    _gun = {
        'MACHINEGUN': 0,
        'MISSILE': 1
    }

    def __init__(self):
        super().__init__()
        self.x = 100
        self.y = 300
        self.shiftx = 0
        self.shifty = 0
        self.height = 25
        self.width = 45
        self.speed = 10 #自機の速さ
        self.image = pygame.image.load("img/fighter4.png")
        self.magazines = copy.copy(Ship._mag)
        self.hit = False

    def disp(self, hitbox=False):
        SURFACE.blit(self.image, (self.x, self.y))
        if hitbox:
            color = (255, 0, 0) if self.hit else (0, 255, 0)
            rect_image = Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(SURFACE, color, rect_image, width=1)

    def get_magazine(self) -> int:
        #現在のマガジンインスタンスを返す
        return self.magazines

    def mag(self):
        #マガジン設定のリストを返す
        return copy.copy(Ship._mag)

    def gun(self):
        #クラス変数の辞書を返す
        return copy.copy(Ship._gun)

    def set_hit_default(self):
        self.hit = False
        return

    def hit_with(self, e=None):
        #接触した
        self.hit = True
        return

    def move(self, keydict):
        self.shiftx = 0
        self.shifty = 0
        if keydict['w'] and self.y > 0:
            self.shifty = -1 * self.speed
        if keydict['a'] and self.x > 0:
            self.shiftx = -1 * self.speed
        if keydict['s'] and self.y + self.height < HEIGHT:
            self.shifty = self.speed
        if keydict['d'] and self.x + self.width < WIDTH:
            self.shiftx = self.speed

        self.x += self.shiftx
        self.y += self.shifty
        return

    def reload(self):
        mags = self.mag()
        for n, mag in enumerate(self.get_magazine()):
            if mag < mags[n]:
                self.magazines[n] += 1
        return


    def shoot(self, type):
        #typeで指定された武器の弾薬クラスを戻り値として返す関数
        #指定された武器が存在するか
        guns = list(self.gun().values())
        if type in guns:
            mag = self.get_magazine()[type]
            max = self.mag()[type]
            #現在残量が必要残量以上かをチェック
            if mag >= max:
                x, y = self.get_location()
                w, h = self.get_size()
                if type == 0:
                    # machinegun
                    bul = Machinegun(x+w, y+h/2)
                    self.magazines[type] -= self.mag()[type]
                elif type == 1:
                    bul = Missile(x+w/2, y+h)
                    self.magazines[type] -= self.mag()[type]
                return bul
            else:
                return None
        else:
            return None
