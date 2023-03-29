import pygame
import random
import math
import 定数表 as c
# 敵キャラクター
ENEMY_NUM = 80                  # 敵キャラクターの個数

# Pygameの初期化
pygame.init()

# 画面の作成
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

# キャラクターの初期位置
character_x = c.SCREEN_WIDTH / 2
character_y = c.SCREEN_HEIGHT / 2

# キャラクターの移動方向
character_direction = (0, 0)


# 敵キャラクターの初期位置
enemies = []
for i in range(ENEMY_NUM):  #配列を用意
    enemy_x = random.randint(0, c.SCREEN_WIDTH - c.CHARACTER_WIDTH)
    enemy_y = random.randint(0, c.SCREEN_HEIGHT - c.CHARACTER_HEIGHT)
    enemy_speed = c.ENEMY_SPEED
    enemy_direction = pygame.math.Vector2(0, 0)
    enemies.append((enemy_x, enemy_y, enemy_speed, enemy_direction))


    #　スプライトの定義
    # 自キャラ　
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(c.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (c.CHARACTER_WIDTH / 1, c.CHARACTER_HEIGHT / 1)   
        self.direction = (0,0)
        self.character_x =0
        self.character_y =0

    def update(self):    
        # マウスの座標を取得
        mouse_x, mouse_y = pygame.mouse.get_pos()

       # キャラクターの移動
        dx = mouse_x - self.character_x
        dy = mouse_y - self.character_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance > c.CHARACTER_SPEED * 1:
           self.direction = (dx / distance, dy / distance)
           self.character_x += self.direction[0] * c.CHARACTER_SPEED * 1
           self.character_y += self.direction[1] * c.CHARACTER_SPEED * 1

        # キャラクターが画面外に出ないようにする。
        if self.character_x < 0:
            self.character_x = 0
        elif self.character_x + c.CHARACTER_WIDTH > c.SCREEN_WIDTH:
            self.character_x = c.SCREEN_WIDTH - c.CHARACTER_WIDTH
        if self.character_y < 0:
            self.character_y = 0
        elif self.character_y + c.CHARACTER_HEIGHT > c.SCREEN_HEIGHT:
            self.character_y = c.SCREEN_HEIGHT - c.CHARACTER_HEIGHT
        #座標に入れる。
        self.rect.x = self.character_x
        self.rect.y = self.character_y
#敵キャラ
r=25
class Enemy_sprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (c.RED), (r, r), r)
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = c.ENEMY_SPEED
        self.direction = pygame.math.Vector2(1, 0)
        #self.direction = (0, 0)
        #以降ローカル変数
        self.collided = False
        self.colidvector = pygame.math.Vector2(1, 0)
        self.localx = x
        self.localy = y

    def update(self):
        self.localx  += self.direction[0] * self.speed
        self.localy  += self.direction[1] * self.speed
        
        # 敵キャラクターが画面外に出ないようにする
        if   self.localx < 0:
            self.localx = 0
        elif self.localx + c.CHARACTER_WIDTH > c.SCREEN_WIDTH:
            self.localx = c.SCREEN_WIDTH - c.CHARACTER_WIDTH
        if   self.localy < 0:
            self.localy = 0
        elif self.localy + c.CHARACTER_HEIGHT > c.SCREEN_HEIGHT:
            self.localy = c.SCREEN_HEIGHT - c.CHARACTER_HEIGHT
        
        self.rect.x  =  self.localx     
        self.rect.y  =  self.localy

    def buruburu(self):
        enemy_x =  self.localx
        enemy_y =  self.localy
        enemy_direction = pygame.math.Vector2(self.direction)
        enemy_speed = self.speed
        enemy_collided = self.collided

        character_x =player.rect.x 
        character_y =player.rect.y 

        #
        dx = character_x - enemy_x
        dy = character_y - enemy_y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        #遠すぎると近付き方向
        if distance > 200:
            rnd1 = random.choice([-2,-1,0,0,2,2])
            rnd2 = random.choice([-2,-1,0,0,2,2])
            enemy_direction = (rnd1 * dx / distance, rnd2 * dy / distance)
            enemy_speed = c.ENEMY_SPEED
            #遠いと離れ方向
        elif distance > 100:
            rnd1 = random.choice([-3,-1,-1,-1,3,3])
            rnd2 = random.choice([-3,-1,-1,-1,3,3])
            enemy_direction = (rnd1 * dx / distance, rnd2 * dy / distance)
            #enemy_direction = pygame.math.Vector2(enemy_direction) #(10*math.pi / 180)
            #enemy_direction.rotate_ip( rnd * 10 *math.pi / 180)
            enemy_speed = c.ENEMY_SPEED
        #基本は逃げてく
        elif distance > 0:
            rnd1 = random.choice([-3,1,-1,1,-3,-3])
            rnd2 = random.choice([-3,-1,1,-1,3,-3])
            enemy_direction = (rnd1 * dx / distance, rnd2 * dy / distance)
            #近いと速く逃げる
            if distance < c.ENEMY_DETECT_RADIUS:
                enemy_speed = c.ENEMY_CHASE_SPEED
            else:
                enemy_speed = c.ENEMY_SPEED


        #ぶつかっていたら反対に逃げる
        if enemy_collided == True:
            enemy_direction =  pygame.math.Vector2(enemy_direction) #(10*math.pi / 180)
            enemy_direction.rotate_ip(5*math.pi / 180)
            enemy_speed = c.ENEMY_DASH_SPEED
  
        

        #スプライトに入れる  #sprite_base
        self.localx = enemy_x
        self.localy = enemy_y
        self.direction = pygame.math.Vector2(enemy_direction) #(0,0)
        self.speed = enemy_speed #0

    def hit_check(self):
        global score
        # 当たり判定を行う
        if pygame.sprite.collide_rect(player, self) == True:
            #当たったら
            if self.collided == False:  
                self.collided = True    #状態変える
                #反対側の位置を覚えておく
                self.collidvector = self.direction
                     
                print("プレイヤーが敵に当たりました。")   
                # 敵に一回あたったら、１点たす。
                score += 1
                self.change_color(c.BLUE) #状態変える               
        else:
            # 当たっていなかったら当たり準備
            self.collided = False     #状態戻す
            self.change_color(c.RED)  #状態戻す   
                   

    def change_color(self, color):
        self.color = color
        self.image = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (color), (r, r), r)

    def change_speed(self, speed):
        self.speed = speed

    def change_direction(self, direction):
        self.direction = direction


# スプライトグループの設定
all_sprites = pygame.sprite.Group()
enemies_sprites = pygame.sprite.Group()

# 自キャラのスプライトを生成
player = Player()
all_sprites.add(player)

# 敵キャラのスプライトを生成
for i in range(ENEMY_NUM):  # ENEMY_NUM体の敵キャラクターを追加
    enemy_x = random.randint(0, c.SCREEN_WIDTH - c.CHARACTER_WIDTH)
    enemy_y = random.randint(0, c.SCREEN_HEIGHT - c.CHARACTER_HEIGHT)
    enemy_sprite = Enemy_sprite(enemy_x, enemy_y)  # 敵キャラのスプライトを作成
    enemies_sprites.add(enemy_sprite)
    
# フォントの設定
font = pygame.font.SysFont(None, 48)

 # スコアの初期値
score = 0

# ゲームオーバーのテキスト
gameover_text = font.render("Game Over", True, c.BLACK)

# ゲームループ
debug = 0
while True:
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

 
    # 敵キャラクターの移動
    for sprites in enemies_sprites: #sprite_base
        
        #ぶるぶる動かしたい場合
        sprites.buruburu()

        #向きを変える動きにしたい場合

        #当たり判定をして、当たった状態を残す。
        sprites.hit_check()

   # 画面の描画
    screen.fill(c.WHITE)

    # スコア表示用Surfaceの作成
    score_surface = font.render(f"Score: {score}", True, c.BLACK)
    score_rect = score_surface.get_rect(center=(c.SCREEN_WIDTH // 2, 50))


   # スプライトの表示
    #pygame.display.flip()         

    enemies_sprites.update()
    all_sprites.update()
    
    enemies_sprites.draw(screen)
    all_sprites.draw(screen)

    # スコアを画面に描画
    screen.blit(score_surface, score_rect)

    # 画面の更新
    pygame.display.update()
