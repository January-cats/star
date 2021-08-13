# -*- coding:utf-8 -*-
#地形を記述する関係にあるクラスを記述

import pygame
from pygame.locals import Rect
import csv

from Entity import Entity
from Settings import WIDTH, HEIGHT, INFO_AREA, SURFACE, SCROLL_SPEED

class FieldPart(Entity):
    #地形パーツだよ
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.color = (0, 255, 0)
        self.hp = 127

    def move(self):
        self.x -= SCROLL_SPEED #地形を左に動かす

    def disp(self):
        rect_image = Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(SURFACE, self.color, rect_image)

    def collision(self, en) -> bool:
        #FieldPart
        x = en.x
        y = en.y
        w = en.width
        h = en.height
        r = ((x >= self.x and x <= self.x + self.width)or\
        (x < self.x and self.x < x + w)) and \
        ((y >= self.y and y <= self.y + self.height)or\
        (y < self.y and self.y < y+h))
        return r

class Field():
    WALL = 80
    DWIDTH = 10 #分割された長方形の幅
    #FieldPartをまとめたクラス
    def __init__(self):
        self.blocks = [] # 現在画面に表示する地形を格納する、上のパーツと下のパーツに分けて配置（リスト）
        self.field = [] # あらかじめ設定された地形情報を格納する、[上, 下]の二次元リスト
        self.progress = 0 #進んだFieldPartの数
        self.tick = 0 #同じFieldPartにおいて、進んだフレーム数
        for i in range(Field.WALL+1): #横に並んだ長方形で初期化、上下それぞれ、スクロール用に右に余分に一つ作る
            upper = FieldPart(i*10, 0, Field.DWIDTH, 50)
            lower = FieldPart(i*10, 550, Field.DWIDTH, 50)
            self.blocks.append([upper, lower]) #初期地形の初期化
            self.field.append([-10, 610])#初期のフィールドを上下フリーにする


    def get_progress(self):
        #progress変数を返す
        return self.progress

    def get_tick(self):
        #tick変数を返す
        return self.tick

    def disp(self):
        #インスタンスを描画する
        SURFACE.fill((0, 0, 0)) #廃液を黒で染める
        for block in self.blocks: #地形の場所を緑で表示
            block[0].disp() #FieldPartクラスのdisp()
            block[1].disp()

    def collision(self, entity):
        #entityと、blocksのなかのentityが一つでも接触しているかどうかで判定する
        r = False
        for block in self.blocks:
            #上もしくは下の地形に接触しているかを確認
            if block[0].collision(entity) or block[1].collision(entity):
                r = True
                break
        return r

    def load(self, filename):
        #csvで記述された地形情報を読み込む
        with open(filename, 'r') as f: #ファイルを読み込みモードで開く
            header = next(csv.reader(f)) #ヘッダー部
            reader = csv.reader(f) #データ部
            field = [] #仮の配列
            for row in reader:
                field.append([int(row[0]), int(row[1])])
            if len(field) < 31:
                return
            else:
                #地形情報を追加
                self.field += field
                self.field.append('EOF') #リストの最後にEOF
        return

    def initialize(self):
        #地形を初期状態にする
        for i in range(Field.WALL+1):
            #地形情報を下にブロックを作成する
            upper = FieldPart(i*10, 0, Field.DWIDTH, self.field[i][0])
            lower = FieldPart(i*10, self.field[i][1], Field.DWIDTH, 600 - self.field[i][1])
            self.blocks[i] = [upper, lower]
        return

    def scroll(self):
        #地形を左に動かす
        #読み込んだ右端まで言ったら止まるようにしたい
        self.tick += 1 #進んだフレームを1増やす
        if self.tick == 1023:
            self.tick = 1 # オーバーフロー回避
        if self.field[self.progress + Field.WALL] != 'EOF': #表示されている地形の一つ右を確認
            #地形の終わりじゃないなら左に動かす
            for block in self.blocks:
                block[0].move() #ブロックを左へスクロールさせる
                block[1].move() #上下のブロックを左に動かす
            if self.blocks[0][0].x + Field.DWIDTH <= 0: #一番左側のブロックが画面右側へ消えたら
                for i in range(Field.WALL):
                    self.blocks[i] = self.blocks[i+1] #ブロックを左寄せ
                if self.field[self.progress + Field.WALL + 1] != 'EOF':
                    #新しい分のブロックをリストの右端に追加
                    upper = FieldPart(800, 0, Field.DWIDTH, self.field[self.progress + Field.WALL + 1][0])
                    lower = FieldPart(800, self.field[self.progress + Field.WALL + 1][1], Field.DWIDTH, 600-self.field[self.progress + Field.WALL + 1][1])
                    self.blocks[Field.WALL] = [upper, lower]
                self.progress += 1
                self.tick = 0 # フレーム数を0に戻す
        return
