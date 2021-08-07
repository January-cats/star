# -*- coding:utf-8 -*-
#メイン

import pygame
import sys
from pygame.locals import QUIT, Rect, KEYDOWN,  K_w, K_a, K_s, K_d, K_SPACE


from Entity import Entity
from Ship import Ship
from Bud import Floater, Sinker
from Bullet import Machinegun, Missile
from Bar import Bar, BarWrapper
from Field import Field, FieldPart
from Background import Star
from Settings import WIDTH, HEIGHT, INFO_AREA, SURFACE, FPSCLOCK, FIELD_FILE

def main():
    #init pygame
    pygame.init()
    pygame.key.set_repeat(5, 5)

    #初期化
    ship = Ship(ship_type=1) #自機
    floater1 = Floater(500, 300)
    floater2 = Floater(300, 300)
    sinker = Sinker(500, 460)
    bar_wrapper = BarWrapper()
    machinegun_bar = Bar(20, 20, 100 ,20)
    missile_bar = Bar(20, 60, 100, 20)
    buds = [] #敵の一覧を保持するリスト
    stars = []
    bullets = []
    fps = 20
    for i in range(1, 30):
        star = Star()
        stars.append(star)

    #敵をリストに追加
    buds.append(floater1)
    buds.append(floater2)
    buds.append(sinker)

    #表示するゲージをリストに追加
    bar_wrapper.add(missile_bar)
    bar_wrapper.add(machinegun_bar)

    #地形の初期化
    field = Field()
    field.load(FIELD_FILE) #地形情報の読み込み
    field.initialize()


    while True:
        #初期化
        keydict = {
            'w': False,
            'a': False,
            's': False,
            'd': False,
            'SPACE': False,
            'h': False
            }
        ship.set_hit_default()
        for bud in buds:
            bud.set_hit_default()

        #押されたキーを取得
        key = pygame.key.get_pressed()
        if key[K_w]:
            keydict['w'] = True
        if key[K_a]:
            keydict['a'] = True
        if key[K_s]:
            keydict['s'] = True
        if key[K_d]:
            keydict['d'] = True
        if key[K_SPACE]:
            keydict['SPACE'] = True
        #イベントキューをかくにん
        for event in pygame.event.get():
            if event.type == QUIT:
                #ゲームの強制終了
                pygame.quit()
                sys.exit()

        #自機の移動
        ship.move(keydict)

        #弾の生成
        if keydict['SPACE']:
            bul = ship.shoot(type=ship.gun()['MACHINEGUN'])
            mis = ship.shoot(type=ship.gun()['MISSILE'])
            if bul:
                bullets.append(bul)
            if mis:
                bullets.append(mis)
        ship.reload()

        #星の移動
        for star in stars:
            star.move()

        #弾の移動
        for n, bullet in enumerate(bullets):
            bullet.move()
            if bullet.is_over_display():
                del bullets[n]

        #敵機の移動
        for bud in buds:
            bud.move(field)

        #地形の移動
        field.scroll()

        #弾と敵の当たり判定
        for n, bullet in enumerate(bullets):
            for bud in buds:
                if bud.collision(bullet):
                    bud.damage(bullet.get_damege())
                    bud.hit_with(bullet)
                    del bullets[n]

        #弾と地形の当たり判定
        for n, bullet in enumerate(bullets):
            if field.collision(bullet):
                del bullets[n]

        #敵の体力が無くなったら消滅させる
        for n, bud in enumerate(buds):
            if bud.is_dead():
                del buds[n]

        #敵と自機の当たり判定
        for bud in buds:
            if ship.collision(bud):
                ship.hit_with(bud)

        #地形と自機の当たり判定
        if field.collision(ship):
            ship.hit_with()

        #描画
        field.disp()

        #ゲージの描画
        guns = ship.gun()
        machinegun_bar.set((ship.get_magazine()[guns['MACHINEGUN']]/ship.mag()[guns['MACHINEGUN']])*100)
        missile_bar.set((ship.get_magazine()[guns['MISSILE']]/ship.mag()[guns['MISSILE']])*100)
        bar_wrapper.disp() # ゲージ残量を描画

        for star in stars:
            star.disp()
        for bullet in bullets:
            bullet.disp()
        for bud in buds:
            bud.disp(hitbox=False)
        ship.disp(hitbox=False)

        #budの体力表示（一時的）
        font = pygame.font.SysFont(None, 36)
        s = ''
        for i in buds:
            s += ' {}'.format(i.hp)
        strimage = font.render("Bud: {}".format(s), True, (255, 255, 255))
        SURFACE.blit(strimage, (400, 20))

        #progressとtickを表示
        font = pygame.font.SysFont(None, 36)
        strimage = font.render("Progress: {}".format(field.get_progress()), True, (255, 255, 255))
        SURFACE.blit(strimage, (WIDTH/2, HEIGHT+20))
        font = pygame.font.SysFont(None, 36)
        strimage = font.render("tick: {}".format(field.get_tick()), True, (255, 255, 255))
        SURFACE.blit(strimage, (WIDTH/2, HEIGHT+60))

        #画面更新
        pygame.display.update()
        FPSCLOCK.tick(fps) #画面更新は20fps

if __name__ == "__main__":
    main()
