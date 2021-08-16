# -*- coding:utf-8 -*-
#地形を記述する関係にあるクラスを記述

import pygame
import csv

from Entity import Entity
from Settings import WIDTH, HEIGHT
from Bud import Floater, Sinker

class BudField():
    #bud全体を管理するクラス
    def __init__(self):
        self.bud_list = [] #現在画面に出現しているbudを格納するリスト
        self.bud_field = [] #あらかじめ設定されたbudの出現情報を格納するリスト
        #progressの順にソートし、出現させたものは削除していく

    def get_list(self):
        return self.bud_list

    def get_bud_field(self):
        return self.bud_field

    def add(self, entity):
        self.bud_list.append(entity)

    def delete(self, num):
        #指定された番号のbudをリストから削除する
        del self.bud_list[num]

    def load(self, filename):
        #あらかじめ設定されたcsvファイルを読み込む
        #progress, type, y: progressは1以上
        with open(filename, 'r') as f: #ファイルを読み込みモードで開く
            header = next(csv.reader(f)) #ヘッダー部
            reader = csv.reader(f) #データ部
            bud_field = [] #仮の配列
            for row in reader:
                #ファイルを１行ずつ処理する
                bud_field.append([int(row[0]), int(row[1]), int(row[2])])
            bud_field = sorted(bud_field, reverse=False, key=lambda x: x[0]) #progressに注目して昇順ソート
            self.bud_field = bud_field #インスタンス変数にコピー
            self.bud_field.append('EOF') #リストの最後にEOF
        return

    def spawn(self, progress):
        #引数にprogressを設定、その値に応じでbudを出現（bud_listに追加）させる。同一progressでの二体同時出現は認められない
        if self.bud_field[0] != 'EOF':
            if self.bud_field[0][0] == progress:
                #あらかじめ定められたprogressと一致した時
                type = self.bud_field[0][1]
                y = self.bud_field[0][2]
                if type == 1:
                    #Floater
                    self.add(Floater(WIDTH, y))
                elif type == 2:
                    #Sinker
                    self.add(Sinker(WIDTH, y, 'up'))
                elif type == 3:
                    #DownSinker
                    self.add(Sinker(WIDTH, y, 'down'))
                #bud_fieldの先頭の要素を最後尾へもっていく
                temp = self.bud_field[0]
                del self.bud_field[0]
                self.bud_field.append(temp)
        return

    def disp_all(self, hitbox=False):
        #bud_listの中身を描画する
        for bud in self.bud_list:
            bud.disp(hitbox)
        return

    def move_all(self, field):
        #bud_listの中身を全てmoveさせる
        #左端まで到達したものは削除する
        for n, bud in enumerate(self.bud_list):
            bud.move(field)
            if bud.x + bud.width < 0:
                self.delete(n)
        return
