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

# 敵キャラクターの個数
ENEMY_NUM = 40

# 敵キャラクターの速度
ENEMY_SPEED = 0.2

#敵キャラクターがプレイヤーキャラクターを検出する範囲の半径
ENEMY_DETECT_RADIUS = 20

# プレイヤーが近くにいる場合に敵キャラクターが追いかける速度
ENEMY_CHASE_SPEED = 0.4

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
    
# フォントの設定
font = pygame.font.SysFont(None, 48)

# ゲームオーバーのテキスト
gameover_text = font.render("Game Over", True, BLACK)

# ゲームループ
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

    # 敵キャラクターの移動
    # キャラクターと敵キャラクターの距離に応じた速度で移動する
    for i in range(len(enemies)):
        enemy_x, enemy_y, enemy_speed, enemy_direction = enemies[i]
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
        if enemy_x < 20:
            enemy_direction = (1, enemy_direction[1])
        elif enemy_x > SCREEN_WIDTH - 20:
            enemy_direction = (-1, enemy_direction[1])
        elif enemy_y < 20:
            enemy_direction = (enemy_direction[0], 1)
        elif enemy_y > SCREEN_HEIGHT - 20:
            enemy_direction = (enemy_direction[0], -1)
        elif random.random() < 0.1:
            enemy_direction = (random.uniform(-1, 1), random.uniform(-1, 1))

        enemy_x += enemy_direction[0] * enemy_speed
        enemy_y += enemy_direction[1] * enemy_speed
        
        # 敵キャラクターが画面外に出たら、反対側から出るようにする
        if   enemy_x < 0:
            enemy_x = 0
        elif enemy_x + CHARACTER_WIDTH > SCREEN_WIDTH:
            enemy_x = SCREEN_WIDTH - CHARACTER_WIDTH
        if   enemy_y < 0:
            enemy_y = 0
        elif enemy_y + CHARACTER_HEIGHT > SCREEN_HEIGHT:
            enemy_y = SCREEN_HEIGHT - CHARACTER_HEIGHT
        enemies[i] = (enemy_x, enemy_y, enemy_speed, enemy_direction)


   # 画面の描画
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, [character_x, character_y, CHARACTER_WIDTH, CHARACTER_HEIGHT])
    #pygame.draw.rect(screen, RED  , [enemy_x, enemy_y, CHARACTER_WIDTH, CHARACTER_HEIGHT])
    for i in range(len(enemies)):
        enemy_x, enemy_y, enemy_speed, enemy_direction = enemies[i]
        pygame.draw.circle(screen, RED, (enemy_x + CHARACTER_WIDTH/2, enemy_y + CHARACTER_HEIGHT/2), CHARACTER_WIDTH/2)

    # 画面の更新
    pygame.display.update()