# -*- coding:utf-8 -*-
#グローバル変数をここに記述

import pygame
from pygame.locals import QUIT, Rect, KEYDOWN,  K_w, K_a, K_s, K_d, K_SPACE, K_h

#画面描画
WIDTH = 800
HEIGHT = 600 #ゲーム本編を描画するエリア
INFO_AREA = 100 #ゲージ類を表示するエリア
FIELD_FILE = "ftest.csv" #読み込む地形ファイル
SCROLL_SPEED = 2 #画面のスクロール速度

#画像ディレクトリのパス
IMG_DIR = "img/"
#地形を除く各エンティティのステータス
SHIP_TYPE = {
    'TYPE1': {
        #自機タイプ1
        'hp': 100,
        'width': 45,
        'height': 25,
        'img': IMG_DIR + "fighter4.png",
        'mag': [5, 15] #machinegun, missile
    },
    'TYPE2': {
        #自機タイプ2
        'hp': 100,
        'width': 50,
        'height': 20,
        'img': IMG_DIR + "fighter5.png",
        'mag': [3, 25] #machinegun, missile
    }
}
FLOATER = {
    #敵キャラクター
    'hp': 100,
    'width': 40,
    'height': 40,
    'img': IMG_DIR + "floater.png"
}
SINKER = {
    #敵キャラクター
    'hp': 150,
    'width': 50,
    'height': 40,
    'img': IMG_DIR + "sinker.png"
}


SURFACE = pygame.display.set_mode((WIDTH, HEIGHT+INFO_AREA))
FPSCLOCK = pygame.time.Clock()
