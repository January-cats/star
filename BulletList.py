# -*- coding:utf-8 -*-
#地形を記述する関係にあるクラスを記述

import pygame
import csv

from Entity import Entity
from Settings import WIDTH, HEIGHT
from Bullet import Bullet

class BulletList():
    def __init__(self):
        self.bullet_list = [] #現在表示されているbulletのリスト
        return

    def get_list(self):
        return self.bullet_list

    def add(self, bullet):
        if bullet:
            #Noneかどうかをチェックする
            self.bullet_list.append(bullet)
        return

    def delete(self, num):
        #指定された番号の要素を削除する
        del self.bullet_list[num]

    def disp_all(self):
        #リストに格納されているエンティティを全て表示させる
        for bul in self.bullet_list:
            bul.disp()

    def move_all(self):
        for n, bul in enumerate(self.bullet_list):
            bul.move()
            if bul.is_over_display():
                self.delete(n)
