# -*- coding:utf-8 -*-
#グローバル変数をここに記述

import pygame
from pygame.locals import QUIT, Rect, KEYDOWN,  K_w, K_a, K_s, K_d, K_SPACE, K_h

#画面描画
WIDTH = 800
HEIGHT = 600 #ゲーム本編を描画するエリア
INFO_AREA = 100 #ゲージ類を表示するエリア
FIELD_FILE = "ftest.csv" #読み込む地形ファイル
BUD_FILE = "btest.csv"
SCROLL_SPEED = 2 #画面のスクロール速度
FPSTICK = 30 #FRAME PER SECOND
HITBOX = 0 #Trueで当たり判定可視化

#地形ダメージ
FIELD_DAMAGE = 1

#画像ディレクトリのパス
IMG_DIR = "img/"
#弾の画像
IMG_MACHINEGUN = IMG_DIR + "bullet.png"
IMG_MISSILE = IMG_DIR + "missile.png"
IMG_SINKER_BULLET = IMG_DIR + "sinker_bullet.png"
IMG_DOWN_MISSILE = IMG_DIR + "downmissile.png"
#地形を除く各エンティティのステータス
SHIP_TYPE = {
    'TYPE1': {
        #自機タイプ1
        'hp': 10000,
        'width': 45,
        'height': 25,
        'img': IMG_DIR + "fighter4.png",
        'mag': [5, 15, 15] #machinegun, missile, downmissile
    },
    'TYPE2': {
        #自機タイプ2
        'hp': 100,
        'width': 50,
        'height': 20,
        'img': IMG_DIR + "fighter5.png",
        'mag': [4, 25, 25] #machinegun, missile, downmissile
    }
}
FLOATER = {
    #敵キャラクター
    'hp': 100,
    'width': 40,
    'height': 40,
    'img': IMG_DIR + "floater.png"
}
SINKER_UP = {
    #敵キャラクター
    'hp': 150,
    'width': 50,
    'height': 40,
    'img': IMG_DIR + "sinker.png", #ウエムキ
    'mag': 60, #弾を出す感覚
}
SINKER_DOWN = {
    #敵キャラクター
    'hp': 150,
    'width': 50,
    'height': 40,
    'img': IMG_DIR + "down_sinker.png", #下向き,
    'mag': 60, #弾を出す感覚
}
BIG_BUD = {
    #敵キャラクター
    'hp': 500,
    'width': 200,
    'height': 132,
    'img': IMG_DIR + "BigBud_l.png",
    'mag': 60, #弾を出す感覚
}
BUD_TYPE={
    1: FLOATER,
    2: SINKER_UP,
    3: SINKER_DOWN,
    4: BIG_BUD,
}


SURFACE = pygame.display.set_mode((WIDTH, HEIGHT+INFO_AREA))
FPSCLOCK = pygame.time.Clock()
