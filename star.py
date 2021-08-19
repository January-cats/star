# -*- coding:utf-8 -*-
#メイン

import pygame
import sys
from pygame.locals import QUIT, KEYDOWN,  K_w, K_a, K_s, K_d, K_h, K_SPACE, K_r

from Entity import Entity
from Ship import Ship
from Bud import Floater, Sinker
from Bullet import Machinegun, Missile
from Bar import Bar, BarWrapper
from Field import Field, FieldPart
from Background import StarParticle
from BudField import BudField
from BulletList import BulletList
from Settings import WIDTH, HEIGHT, INFO_AREA, SURFACE, FPSCLOCK, FIELD_FILE, BUD_FILE, HITBOX, FPSTICK, FIELD_DAMAGE
from Settings import SHIP_TYPE #ゲージの描画に使う

class StarManager():
    #ゲームの状態変数
    TITLE = 1 #タイトル画面
    PLAY = 2 #ゲームプレイ画面
    GAME_OVER = 3 #ゲームオーバー画面

    #ゲームオーバーなど、ゲームの状態、および各インスタンスを管理する
    def __init__(self):
        #初期化
        self.ship = Ship(ship_type=1)

        #ゲージ
        self.bar_wrapper = BarWrapper()
        ship_hp_bar = Bar(20, 20, 200 ,20)
        #表示するゲージをリストに追加
        self.bar_wrapper.add(ship_hp_bar)

        #地形の初期化
        self.field = Field()
        self.field.load(FIELD_FILE) #地形情報の読み込み
        self.field.initialize()

        #budの初期化
        self.bud_field = BudField() #budを管理するクラスのインスタンス
        self.bud_field.load(BUD_FILE)

        self.stars = [] #背景の星のリスト
        for i in range(1, 30):
            star = StarParticle()
            self.stars.append(star)
        self.bullet_list = BulletList() #自機の弾リスト
        self.bud_bullet_list = BulletList() #敵の弾リスト

        #ゲームの状態変数
        self.idx = StarManager.TITLE

    def backup(ship, bar_wrapper, stars, bullet_list, bud_bullet_list, field, bud_field, idx):
        # Ship, BarWrapper, stars, bullet_list, bud_bullet_list, field, bud_field, の8つを管理、バックアップできるように
        self.ship = ship
        self.bar_wrapper = bar_wrapper
        self.stars = stars
        self.bullet_list = bullet_list
        self.bud_bullet_list = bud_bullet_list
        self.field = field
        self.bud_field = bud_field
        self.idx = idx
        return 0

    def read(self):
        d = {
            'ship': self.ship,
            'bar_wrapper': self.bar_wrapper,
            'stars': self.stars,
            'bullet_list': self.bullet_list,
            'bud_bullet_list': self.bud_bullet_list,
            'field': self.field,
            'bud_field': self.bud_field,
            'idx': self.idx
        }
        return d

class Star():

    #ゲーム本体を管理するクラス
    def __init__(self):
        self.manager = StarManager()

    def star(self):
        #データ読み込み
        data = self.manager.read()
        ship = data['ship']
        bar_wrapper = data['bar_wrapper']
        stars = data['stars']
        field = data['field']
        bud_field = data['bud_field']
        bullet_list = data['bullet_list']
        bud_bullet_list = data['bud_bullet_list']
        idx = data['idx']

        #サブウェポン変更変数
        subweapon_change = False

        keydict = {
            'w': False,
            'a': False,
            's': False,
            'd': False,
            'SPACE': False,
            'h': False,
            'ESCAPE': False
            }

        while True:
            if idx == StarManager.TITLE:
                SURFACE.fill((0, 0, 0))
                font = pygame.font.SysFont(None, 36)
                strimage = font.render("Press SPACE to start", True, (255, 255, 255))
                center_str = strimage.get_rect(center=(WIDTH/2, HEIGHT/2))
                SURFACE.blit(strimage, center_str)

                #イベントキューをかくにん
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            idx = StarManager.PLAY
                    if event.type == QUIT:
                        #ゲームの強制終了
                        pygame.quit()
                        sys.exit()

            elif idx == StarManager.GAME_OVER:
                #-----------ゲームオーバーになった時の処理--------------
                SURFACE.fill((0, 0, 0))
                font = pygame.font.SysFont(None, 36)
                strimage = font.render("Game Over (Press r to return title)", True, (255, 255, 255))
                center_str = strimage.get_rect(center=(WIDTH/2, HEIGHT/2))
                SURFACE.blit(strimage, center_str)

                #イベントキューをかくにん
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_r:
                            return 'r'
                    if event.type == QUIT:
                        #ゲームの強制終了
                        pygame.quit()
                        sys.exit()
            elif idx == StarManager.PLAY:
                #ゲームプレイ中の処理
                #初期化
                keydict['w'] = False
                keydict['a'] = False
                keydict['s'] = False
                keydict['d'] = False
                keydict['SPACE'] = False
                keydict['ESCAPE'] = False

                ship.set_hit_default()
                for bud in bud_field.get_list():
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
                #hキーが押された時に一回だけ動作する
                if not key[K_h]:
                    keydict['h'] = False
                elif not keydict['h']:
                    keydict['h'] = True
                    ship.change_subweapon() #武器の切り替え
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
                    bullet_list.add(bul)
                    if ship.get_subweapon() == 1:
                        mis = ship.shoot(type=ship.gun()['MISSILE'])
                        bullet_list.add(mis)
                    if ship.get_subweapon() == 2:
                        dmis = ship.shoot(type=ship.gun()['DOWN_MISSILE'])
                        bullet_list.add(dmis)
                ship.reload()

                #budの射撃
                for bud in bud_field.get_list():
                    bul = bud.shoot(ship)
                    if bul:
                        bud_bullet_list.add(bul)
                    bud.reload()

                #星の移動
                for star in stars:
                    star.move()

                #弾の移動
                bullet_list.move_all() #自機
                bud_bullet_list.move_all() #敵

                #敵機の移動
                bud_field.move_all(field)

                #地形の移動
                field.scroll()

                #budの出現
                if field.get_tick() == 0:
                    bud_field.spawn(field.get_progress())

                #-----------当たり判定のチェック----------

                #弾と敵の当たり判定
                for n, bullet in enumerate(bullet_list.get_list()):
                    for bud in bud_field.get_list():
                        if bud.collision(bullet):
                            bud.damage(bullet.get_damege())
                            bud.hit_with(bullet)
                            bullet_list.delete(n)

                #敵の弾と自機との当たり判定
                for n, bullet in enumerate(bud_bullet_list.get_list()):
                    if ship.collision(bullet):
                        #自機が敵の弾と接触していたら
                        ship.do_damage(bullet.get_damege())
                        ship.hit_with(bullet)
                        bud_bullet_list.delete(n)

                #弾と地形の当たり判定
                for n, bullet in enumerate(bullet_list.get_list()):
                    if field.collision(bullet):
                        bullet_list.delete(n)

                #敵の弾と地形の当たり判定
                for n, bullet in enumerate(bud_bullet_list.get_list()):
                    if field.collision(bullet):
                        bud_bullet_list.delete(n)

                #敵と自機の当たり判定
                for bud in bud_field.get_list():
                    if ship.collision(bud):
                        ship.do_damage(FIELD_DAMAGE)
                        ship.hit_with(bud)

                #地形と自機の当たり判定
                if field.collision(ship):
                    ship.hit_with()
                    ship.do_damage(FIELD_DAMAGE)

                #----------体力判定---------------
                #自機の体力がなくなったらゲームオーバーにする
                if ship.get_hp() <= 0:
                    idx = StarManager.GAME_OVER

                #敵の体力が無くなったら消滅させる
                for n, bud in enumerate(bud_field.get_list()):
                    if bud.is_dead():
                        bud_field.delete(n)

                #--------------各要素の描画-----------------

                #地形を描画
                field.disp()

                #自機の体力ゲージの描画
                ship_type = ship.get_type()
                bar_wrapper.bar_list[0].set((ship.get_hp()/SHIP_TYPE[ship_type]['hp'])*100)
                bar_wrapper.disp() # ゲージ残量を描画

                #ゲージと画面の境界線

                for star in stars:
                    star.disp()
                bud_field.disp_all(hitbox=HITBOX)
                bullet_list.disp_all()
                bud_bullet_list.disp_all()
                ship.disp(hitbox=HITBOX)

                #budの体力表示（一時的）
                font = pygame.font.SysFont(None, 36)
                s = ''
                for i in bud_field.get_list():
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
                font = pygame.font.SysFont(None, 36)
                strimage = font.render("weapon: {}".format(ship.get_subweapon()), True, (255, 255, 255))
                SURFACE.blit(strimage, (WIDTH*3/4, HEIGHT+20))
                font = pygame.font.SysFont(None, 36)
                strimage = font.render("final: {}".format(field.do_reach_final()), True, (255, 255, 255))
                SURFACE.blit(strimage, (WIDTH*3/4, HEIGHT+60))

            #---------画面更新--------------

            #画面更新
            pygame.display.update()
            FPSCLOCK.tick(FPSTICK) #画面更新は20fps

        return 0

def main():
    #init pygame
    pygame.init()
    pygame.key.set_repeat(5000, 5)

    star = Star()

    while 1:
        star.__init__()
        res = star.star()
        if res == 'r':
            continue

    return 0

if __name__ == "__main__":
    main()
