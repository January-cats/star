# -*- coding:utf-8 -*-
#グローバル変数をここに記述

import pygame
from pygame.locals import QUIT, Rect, KEYDOWN,  K_w, K_a, K_s, K_d, K_SPACE, K_h

WIDTH = 800
HEIGHT = 600 #ゲーム本編を描画するエリア
INFO_AREA = 100 #ゲージ類を表示するエリア

SURFACE = pygame.display.set_mode((WIDTH, HEIGHT+INFO_AREA))
FPSCLOCK = pygame.time.Clock()
