# -*- coding:utf-8 -*-
#グローバル変数をここに記述

import pygame
from pygame.locals import QUIT, Rect, KEYDOWN,  K_w, K_a, K_s, K_d, K_SPACE, K_h

#画面描画
WIDTH = 800
HEIGHT = 600 #ゲーム本編を描画するエリア
INFO_AREA = 100 #ゲージ類を表示するエリア
FIELD_FILE = "ftest.csv"

#画像ディレクトリのパス
IMG_DIR = "img/"
#地形を除く各エンティティのステータス
FLOATER = {
    'hp': 100,
    'width': 40,
    'height': 40,
    'img': IMG_DIR + "floater.png"
}
SINKER = {
    'hp': 150,
    'width': 50,
    'height': 40,
    'img': IMG_DIR + "sinker.png"
}


SURFACE = pygame.display.set_mode((WIDTH, HEIGHT+INFO_AREA))
FPSCLOCK = pygame.time.Clock()
