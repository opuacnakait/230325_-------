import pygame
import random
import math

# 画面のサイズ
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# キャラクターのサイズ
CHARACTER_WIDTH = 50
CHARACTER_HEIGHT = 50

# キャラクターの速度
CHARACTER_SPEED = 5

# 敵キャラクター
ENEMY_NUM = 40                  # 敵キャラクターの個数
ENEMY_SPEED = 0.2               # 敵キャラクターの速度
ENEMY_DETECT_RADIUS = 20        # 敵キャラクターがプレイヤーキャラクターを検出する範囲の半径
ENEMY_CHASE_SPEED = 0.4         # プレイヤーが近くにいる場合に敵キャラクターが追いかける速度


# 色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Pygameの初期化
pygame.init()

# 画面の作成
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# キャラクターの初期位置
character_x = SCREEN_WIDTH / 2
character_y = SCREEN_HEIGHT / 2

# キャラクターの移動方向
character_direction = (0, 0)


# 敵キャラクターの初期位置
enemies = []
for i in range(ENEMY_NUM):  # 3体の敵キャラクターを追加
    enemy_x = random.randint(0, SCREEN_WIDTH - CHARACTER_WIDTH)
    enemy_y = random.randint(0, SCREEN_HEIGHT - CHARACTER_HEIGHT)
    enemy_speed = ENEMY_SPEED
    enemy_direction = (0, 0)
    enemies.append((enemy_x, enemy_y, enemy_speed, enemy_direction))


    #　スプライトの定義
    # 自キャラ　
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (CHARACTER_WIDTH / 1, CHARACTER_HEIGHT / 1)   
#敵キャラ
r=25
class Enemy_sprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (r, r), r)
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        """
        self.rect.width = CHARACTER_WIDTH*2  # ここを追加
        self.rect.height = CHARACTER_HEIGHT*2  # ここを追加
        """
        self.speed = ENEMY_SPEED
        self.direction = (0, 0)

# スプライトグループの設定
all_sprites = pygame.sprite.Group()
enemies_sprites = pygame.sprite.Group()

# 自キャラ
player = Player()
all_sprites.add(player)

# 敵キャラ
for i in range(ENEMY_NUM):  # ENEMY_NUM体の敵キャラクターを追加
    enemy_x = random.randint(0, SCREEN_WIDTH - CHARACTER_WIDTH)
    enemy_y = random.randint(0, SCREEN_HEIGHT - CHARACTER_HEIGHT)
    enemy_sprite = Enemy_sprite(enemy_x, enemy_y)  # 敵キャラのスプライトを作成
    enemies_sprites.add(enemy_sprite)
    #all_sprites.add(enemy_sprite)
   
# フォントの設定
font = pygame.font.SysFont(None, 48)

# ゲームオーバーのテキスト
gameover_text = font.render("Game Over", True, BLACK)

# ゲームループ
debug = 0
while True:
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # マウスの座標を取得
    mouse_x, mouse_y = pygame.mouse.get_pos()

   # キャラクターの移動
    dx = mouse_x - character_x
    dy = mouse_y - character_y
    distance = (dx ** 2 + dy ** 2) ** 0.5
    if distance > CHARACTER_SPEED * 0.5:
        character_direction = (dx / distance, dy / distance)
        character_x += character_direction[0] * CHARACTER_SPEED * 0.5
        character_y += character_direction[1] * CHARACTER_SPEED * 0.5

    # キャラクターが画面外に出たら、反対側から出るようにする
    if character_x < 0:
        character_x = 0
    elif character_x + CHARACTER_WIDTH > SCREEN_WIDTH:
        character_x = SCREEN_WIDTH - CHARACTER_WIDTH
    if character_y < 0:
        character_y = 0
    elif character_y + CHARACTER_HEIGHT > SCREEN_HEIGHT:
        character_y = SCREEN_HEIGHT - CHARACTER_HEIGHT
    #スプライトに入れる
    player.rect.x = character_x
    player.rect.y = character_y
     
    # 敵キャラクターの移動
    # キャラクターと敵キャラクターの距離に応じた速度で移動する
    for i in range(len(enemies)):
    #for sprites in enemies_sprites:
        enemy_x, enemy_y, enemy_speed, enemy_direction = enemies[i]
        #enemy_x =  sprites.rect.x
        #enemy_y =  sprites.rect.y
        #enemy_direction = sprites.direction
        #enemy_speed = sprites.speed

        character_x =player.rect.x 
        character_y =player.rect.y 

        debug +=1
        if debug >3: 
            debug = 0

        dx = character_x - enemy_x
        dy = character_y - enemy_y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            enemy_direction = (-dx / distance, -dy / distance)
            if distance < ENEMY_DETECT_RADIUS:
                enemy_speed = ENEMY_CHASE_SPEED
            else:
                enemy_speed = ENEMY_SPEED


        # 画面端で固まらないように左右にランダムに移動する
        if enemy_x < 0:
            enemy_direction = (1, enemy_direction[1])
        elif enemy_x > SCREEN_WIDTH - 0:
            enemy_direction = (-1, enemy_direction[1])
        elif enemy_y < 0:
            enemy_direction = (enemy_direction[0], 1)
        elif enemy_y > SCREEN_HEIGHT - 0:
            enemy_direction = (enemy_direction[0], -1)
        elif random.random() < 0.1:
            enemy_direction = (random.uniform(-1, 1), random.uniform(-1, 1))

        enemy_x += enemy_direction[0] * enemy_speed
        enemy_y += enemy_direction[1] * enemy_speed
        

        # 敵キャラクターが画面外に出ないようにする
        if   enemy_x < 0:
            enemy_x = 0
        elif enemy_x + CHARACTER_WIDTH > SCREEN_WIDTH:
            enemy_x = SCREEN_WIDTH - CHARACTER_WIDTH
        if   enemy_y < 0:
            enemy_y = 0
        elif enemy_y + CHARACTER_HEIGHT > SCREEN_HEIGHT:
            enemy_y = SCREEN_HEIGHT - CHARACTER_HEIGHT

        #スプライトに入れる
        #sprites.rect.x = enemy_x
        #sprites.rect.y = enemy_y
        #sprites.direction = enemy_direction #(0,0)
        #sprites.speed = enemy_speed #0

        enemies[i] = (enemy_x, enemy_y, enemy_speed, enemy_direction)

    #スプライトの座標を更新
    i=0
    for sprites in enemies_sprites:
        enemy_x, enemy_y, enemy_speed, enemy_direction = enemies[i]
        #スプライトに入れる
        sprites.rect.x = enemy_x
        sprites.rect.y = enemy_y
        sprites.direction =  (0,0) #enemy_direction
        sprites.speed = 0 #enemy_speed #0
        i +=1
        
   # 画面の描画
    screen.fill(WHITE)
    
   # スプライトの表示
    #pygame.display.flip()         
    #all_sprites.update()
    
    enemies_sprites.draw(screen)
    all_sprites.draw(screen)
    
    # 画面の更新
    pygame.display.update()
