# -*- coding:utf-8 -*-

import pygame
import sys
from pygame.locals import QUIT, Rect, KEYDOWN,  K_w, K_a, K_s, K_d, K_SPACE, K_h
from random import randint
import copy
import csv


from Entity import Entity

#init pygame
pygame.init()
pygame.key.set_repeat(5, 5)
WIDTH = 800
HEIGHT = 600 #ゲーム本編を描画するエリア
INFO_AREA = 100 #ゲージ類を表示するエリア
SURFACE = pygame.display.set_mode((WIDTH, HEIGHT+INFO_AREA))
FPSCLOCK = pygame.time.Clock()

class Ship(Entity):
    _mag = [
        5, # machinegun
        15, # missile
    ]
    #武器ナンバ
    _gun = {
        'MACHINEGUN': 0,
        'MISSILE': 1
    }

    def __init__(self):
        super().__init__()
        self.x = 100
        self.y = 300
        self.shiftx = 0
        self.shifty = 0
        self.height = 25
        self.width = 45
        self.speed = 10 #自機の速さ
        self.image = pygame.image.load("img/fighter4.png")
        self.magazines = copy.copy(Ship._mag)
        self.hit = False

    def disp(self, hitbox=False):
        SURFACE.blit(self.image, (self.x, self.y))
        if hitbox:
            color = (255, 0, 0) if self.hit else (0, 255, 0)
            rect_image = Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(SURFACE, color, rect_image, width=1)

    def get_magazine(self) -> int:
        #現在のマガジンインスタンスを返す
        return self.magazines

    def mag(self):
        #マガジン設定のリストを返す
        return copy.copy(Ship._mag)

    def gun(self):
        #クラス変数の辞書を返す
        return copy.copy(Ship._gun)

    def set_hit_default(self):
        self.hit = False
        return

    def hit_with(self, e=None):
        #接触した
        self.hit = True
        return

    def move(self, keydict):
        self.shiftx = 0
        self.shifty = 0
        if keydict['w'] and self.y > 0:
            self.shifty = -1 * self.speed
        if keydict['a'] and self.x > 0:
            self.shiftx = -1 * self.speed
        if keydict['s'] and self.y + self.height < HEIGHT:
            self.shifty = self.speed
        if keydict['d'] and self.x + self.width < WIDTH:
            self.shiftx = self.speed

        self.x += self.shiftx
        self.y += self.shifty
        return

    def reload(self):
        mags = self.mag()
        for n, mag in enumerate(self.get_magazine()):
            if mag < mags[n]:
                self.magazines[n] += 1
        return


    def shoot(self, type):
        #typeで指定された武器の弾薬クラスを戻り値として返す関数
        #指定された武器が存在するか
        guns = list(self.gun().values())
        if type in guns:
            mag = self.get_magazine()[type]
            max = self.mag()[type]
            #現在残量が必要残量以上かをチェック
            if mag >= max:
                x, y = self.get_location()
                w, h = self.get_size()
                if type == 0:
                    # machinegun
                    bul = Machinegun(x+w, y+h/2)
                    self.magazines[type] -= self.mag()[type]
                elif type == 1:
                    bul = Missile(x+w/2, y+h)
                    self.magazines[type] -= self.mag()[type]
                return bul
            else:
                return None
        else:
            return None

class Bullet(Entity):
    def __init__(self, x, y):
        #初期化
        super().__init__()
        self.x = x
        self.y = y
        self.width = 5 #弾の大きさ
        self.height = 5
        self.speed = 20
        self.image = None
        self.damage = 10

    def disp(self, hitbox=False):
        SURFACE.blit(self.image, (self.x, self.y))
        if hitbox:
            rect_image = Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(SURFACE, (0, 255, 0), rect_image, width=2)
        return

    def move(self):
        self.x += self.speed

    def is_over_display(self):
        return WIDTH <= self.x

class Machinegun(Bullet):
    #弾クラスを継承したマシンガンクラス
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 20
        self.height = 5
        self.width = 5
        self.damage = 10
        self.image = pygame.image.load("img/bullet.png")

class Missile(Bullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 0
        self.height = 6
        self.width = 15
        self.damage = 20
        self.image = pygame.image.load("img/missile.png")

    def move(self):
        self.x += self.speed
        self.speed = self.speed + 3
        return

class Star(Entity):
    def __init__(self):
        super().__init__()
        self.x = randint(1, WIDTH)
        self.y = randint(0, HEIGHT)
        self.xv = randint(1, 10)
        self.color = (255, 255, 255)

    def disp(self):
        rect_image = Rect(self.x, self.y, 2, 2)
        pygame.draw.rect(SURFACE, self.color, rect_image)

    def move(self):
        self.x -= self.xv
        if self.x <= 0:
            self.x = WIDTH
            self.y = randint(0, HEIGHT)
            self.xv = randint(1, 10)

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
        self.x -= 1

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

class Bud(Entity):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.image = pygame.image.load("img/floater.png")
        self.hp = 100
        self.speed = 5
        self.hit = False

    def disp(self, hitbox=False):
        SURFACE.blit(self.image, (self.x, self.y))
        if hitbox:
            color = (255, 0, 0) if self.hit else (0, 255, 0)
            rect_image = Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(SURFACE, color, rect_image, width=1)

    def move(self, field):
        pass

    def damage(self, num):
        self.hp -= num
        return

    def is_dead(self):
        return self.hp <= 0

    def set_hit_default(self):
        #接触していない
        self.hit = False
        return

    def hit_with(self, e):
        #接触した
        self.hit = True
        return

class Floater(Bud):
    #浮いてる敵キャラ
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.image = pygame.image.load("img/floater.png")
        self.hp = 100
        self.speed = 5
        self.hit = False

    def move(self, field):
        self.y += self.speed
        if field.collision(self):
            self.speed = self.speed * (-1)
        elif self.y <= 0 or self.y+self.height >= HEIGHT:
            self.speed = self.speed * (-1)

class Sinker(Bud):
    #地面にいる敵キャラ
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 40
        self.image = pygame.image.load("img/sinker.png")
        self.hp = 150
        self.speed = 5
        self.hit = False

    def move(self, field):
        self.x -= 1


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
            self.blocks.append([upper, lower])

    def get_progress(self):
        return self.progress

    def get_tick(self):
        return self.tick

    def disp(self):
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
                self.field = field
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
        if self.tick == 1024:
            self.tick = 1 # オーバーフロー回避
        if self.field[self.progress + Field.WALL] != 'EOF': #表示されている地形の一つ右を確認
            #地形の終わりじゃないなら左に動かす
            for block in self.blocks:
                block[0].move()
                block[1].move() #上下のブロックを左に動かす
            if self.blocks[0][0].x + Field.DWIDTH <= 0: #一番左側のブロックが画面右側へ消えたら
                for i in range(Field.WALL):
                    self.blocks[i] = self.blocks[i+1] #ブロックを左寄せ
                if self.field[self.progress + Field.WALL + 1] != 'EOF':
                    #新しい分のブロックを追加
                    upper = FieldPart(800, 0, Field.DWIDTH, self.field[self.progress + Field.WALL + 1][0])
                    lower = FieldPart(800, self.field[self.progress + Field.WALL + 1][1], Field.DWIDTH, 600-self.field[self.progress + Field.WALL + 1][1])
                    self.blocks[Field.WALL] = [upper, lower]
                self.progress += 1
                self.tick = 0 # フレーム数を0に戻す
        return


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

def main():
    #初期化
    ship = Ship() #自機
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
    field.load("ftest.csv") #地形情報の読み込み
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
        if key[K_h]:
            keydict['h'] = True
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
            if bul:
                bullets.append(bul)
        if keydict['h']:
            mis = ship.shoot(type=ship.gun()['MISSILE'])
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
            bud.disp(hitbox=True)
        ship.disp(hitbox=True)

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
