# -*- coding:utf-8 -*-
#Barを記述する関係にあるクラスを記述

import pygame
from pygame.locals import Rect

from Entity import Entity
from Settings import WIDTH, HEIGHT, INFO_AREA, SURFACE

class BarWrapper():
    def __init__(self):
        self.bar_list = [] #Barインスタンスのリスト
        self.info_area = INFO_AREA #情報エリアの高さ

    def disp(self):
        #情報エリア全体を黒で塗りつぶす
        wrapper = Rect(0, HEIGHT, WIDTH, self.info_area)
        pygame.draw.rect(SURFACE, (0, 0, 0), wrapper)
        #ゲージそれぞれを描画する
        for bar in self.bar_list:
            bar.disp()

    def add(self, bar):
        #ゲージをリストに追加する
        self.bar_list.append(bar)

    def length(self):
        return len(self.bar_list)

    def delete(self, num):
        if 0 <= num and num < self.length():
            del self.bar_list[num]

class Bar():
    def __init__(self, x, y, bwidth, bheight): #情報エリアのx, y
        self.x = x
        self.y = HEIGHT + y
        self.width = bwidth #ゲージの幅
        self.height = bheight #ゲージの高さ
        self.num = 0 # 表示するデータ(%)

    def disp(self):
        outer = Rect(self.x, self.y, self.width, self.height)
        inner = Rect(self.x, self.y, self.num, self.height)
        pygame.draw.rect(SURFACE, (255, 255, 0), inner, width=0)
        pygame.draw.rect(SURFACE, (255, 255, 255), outer, width=1)

    def set(self, num):
        #表示するデータをセット
        self.num = num
