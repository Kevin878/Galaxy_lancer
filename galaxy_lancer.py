import pygame
from pygame.locals import *
import math
import random
import sys

BLACK = (0, 0, 0)
SILVER = (192, 208, 224)
RED = (255, 0, 0)
CYAN = (0, 224, 255)
WHITE = (255, 255, 255)

img_sship = [
    pygame.image.load("source/image_gl/starship.png"),
    pygame.image.load("source/image_gl/starship_l.png"),
    pygame.image.load("source/image_gl/starship_r.png"),
    pygame.image.load("source/image_gl/starship_burner.png")
]
img_shield = pygame.image.load("source/image_gl/shield.png")

img_weapon = pygame.image.load("source/image_gl/bullet.png")
img_enemy = [pygame.image.load(f"source/image_gl/enemy{id}.png") for id in range(5)] + [
    pygame.image.load("source/image_gl/enemy_boss.png"),
    pygame.image.load("source/image_gl/enemy_boss_f.png")
]
img_explore = [None] + [pygame.image.load(f"source/image_gl/explosion{i+1}.png") for i in range(5)] #不能讓清單推倒式同時與其他值出現

img_title = [
    pygame.image.load("source/image_gl/nebula.png"),
    pygame.image.load("source/image_gl/logo.png")
]

# 畫面大小
SCREEN_X = 1440
SCREEN_Y = 800

# 載入影像
img_galaxy = pygame.image.load("source/image_gl/galaxy.png")
img_galaxy = pygame.transform.scale(img_galaxy, (960, SCREEN_Y))

# 畫面
FPS = 30
speed = 16 #管理非玩家速度（大局速度）
player_speed = 20

# 玩家數量
PLAYER = 1

# 難度
MODE = ["EASY", "NORMAL", "HARD", "FEARFUL"] #管理難度的列表
mode_number = 0 #管理所選擇的難度

# 背景
idx = -1
tmr = 0
score = 0
highest_score = 10000

bg_y = 0

#管理搖桿操作
joysticks = []
BTdown = [0] * PLAYER
BTup = [0] * PLAYER
BTright = [0] * PLAYER
BTleft = [0] * PLAYER
axis0 = [0] * PLAYER
axis1 = [0] * PLAYER

# 角色
ss_x = [0] * PLAYER
ss_y = [0] * PLAYER
ss_d = [0] * PLAYER
ss_burner = [True] * PLAYER
ss_shield = 100 #防禦力
ss_invincible = [0] * PLAYER #無敵狀態

# 按鍵
Key_Up = 0
Key_Down = 0
Key_Spc = [0] * PLAYER
Key_Z = [0] * PLAYER

# 飛彈
MSL_COLD = 5 #子彈的冷卻時間（幀）
MSL_SPEED = 36 #子彈的移動速度
MSL_MAX = 200 #最多能同時出現的子彈
msl_id = 0 #管理子彈列表的索引值
msl_f = [False] * MSL_MAX #管理是否每一個子彈是否還在畫面內
msl_x = [0] * MSL_MAX 
msl_y = [0] * MSL_MAX
msl_a = [0] * MSL_MAX #管理旋轉的角度

# 敵機
ENEMY_MAX = 100
ENEMY_FRE = 30
emy_id = 0
emy_f = [False] * ENEMY_MAX
emy_x = [0] * ENEMY_MAX
emy_y = [0] * ENEMY_MAX
emy_a = [0] * ENEMY_MAX
emy_type = [0] * ENEMY_MAX
emy_speed = [0] * ENEMY_MAX
emy_shield = [0] * ENEMY_MAX
emy_count = [0] * ENEMY_MAX

# 敵機種類
EMY_BULLET = 0
ENEMY_TYPE = 1
ENEMY_BOSS = 5
dis = 0 #管理魔王機與畫面中央的距離

# 敵機邊界
LINE_T = -40
LINE_B = SCREEN_Y+40
LINE_L = -40
LINE_R = SCREEN_X+40

# 爆炸特效
EFFECT_MAX = 100
eff_id = 0
eff_x = [0] * EFFECT_MAX
eff_y = [0] * EFFECT_MAX
eff_p = [0] * EFFECT_MAX #管理爆炸特效圖片列表的索引值 

# 處理音效
se_barrage = None #發射彈幕的音效
se_damage = None #受到傷害的音效
se_explosion = None #魔王死掉時的音效
se_shot = None #發射飛彈的音效

# 90度 -> cos:0 sin:1  往下
# 180度 -> cos:-1 sin:0 往左
# 270度 -> cos:0 sin:-1 往上
# 360度 or 0度 -> cos:1 sin:0 往右

def move_starship(scrn: pygame.Surface):
    global ss_x, ss_y, ss_d, ss_burner, ss_shield, ss_invincible
    global Key_Spc, Key_Z
    global idx, tmr

    for plid in range(PLAYER):
        ss_d[plid] = 0
        ss_burner[plid] = False

        # 移動邏輯
        if axis1[plid] <= -0.5:
            ss_y[plid] -= player_speed
            ss_burner[plid] = True
            if ss_y[plid] < 80:
                ss_y[plid] = 80
        if axis1[plid] >= 0.5:
            ss_y[plid] += player_speed
            ss_burner[plid] = True
            if ss_y[plid] > SCREEN_Y-80:
                ss_y[plid] = SCREEN_Y-80
        if axis0[plid] <= -0.5:
            ss_x[plid] -= player_speed
            ss_d[plid] = 1
            ss_burner[plid] = True
            if ss_x[plid] < 40:
                ss_x[plid] = 40
        if axis0[plid] >= 0.5:
            ss_x[plid] += player_speed
            ss_d[plid] = 2
            ss_burner[plid] = True
            if ss_x[plid] > SCREEN_X-40:
                ss_x[plid] = SCREEN_X-40

        # 按鍵邏輯
        Key_Spc[plid] = (Key_Spc[plid] + 1) * BTright[plid]
        if Key_Spc[plid] % MSL_COLD == 1:
            set_missile(1, ss_x[plid], ss_y[plid], ss_d[plid])
            se_shot.play()
        Key_Z[plid] = (Key_Z[plid] + 1) * BTdown[plid]
        if Key_Z[plid] == 1 and ss_shield > 10:
            ss_shield -= 10 #扣掉防禦力
            set_missile(10, ss_x[plid], ss_y[plid], ss_d[plid])
            se_barrage.play()

        # 燃燒特效
        if ss_burner[plid]:
            scrn.blit(img_sship[3], [ss_x[plid] - img_sship[3].get_width() // 2, (ss_y[plid] + img_sship[ss_d[plid]].get_height() // 2) + ((tmr % 3) * 2)])

        # 無敵時間
        if ss_invincible[plid] % 3 == 0:
            scrn.blit(img_sship[ss_d[plid]], [ss_x[plid] - img_sship[ss_d[plid]].get_width() // 2, ss_y[plid] - img_sship[ss_d[plid]].get_height() // 2])
            draw_text(scrn, str(plid+1), ss_x[plid], ss_y[plid], 70, WHITE, False)
        
        if ss_invincible[plid] > 0:
            ss_invincible[plid] -= 1
            continue

        # 碰撞邏輯
        elif idx == 1:
            for id in range(ENEMY_MAX):
                if emy_f[id]:
                    w = img_enemy[emy_type[id]].get_width()
                    h = img_enemy[emy_type[id]].get_height()
                    r = int((w + h) / 4 + (74 + 96) / 4)
                    if get_dis(ss_x[plid], ss_y[plid], emy_x[id], emy_y[id]) < r * r:
                        if emy_type[id] not in (5, 6):
                            emy_f[id] = False
                            set_effect(emy_x[id], emy_y[id])
                            se_damage.play()
                        else:
                            if axis0[plid] <= -0.5:
                                ss_x[plid] += 200
                            if axis0[plid] >= 0.5:
                                ss_x[plid] -= 200
                            if axis1[plid] <= -0.5:
                                ss_y[plid] += 200
                            if axis1[plid] >= 0.5:
                                ss_y -= 200
                
                        ss_shield -= 10 / PLAYER
                        if ss_shield < 0:
                            ss_shield = 0
                            idx = 2
                            tmr = 0
                        if ss_invincible[plid] == 0:
                            ss_invincible[plid] = 60


def set_missile(typ, x, y, d):
    global msl_f, msl_x, msl_y, msl_id
    if typ == 1:
        if not msl_f[msl_id]: #當畫面上沒有子彈在飛的話
            msl_f[msl_id] = True
            msl_x[msl_id] = x
            msl_y[msl_id] = y-img_sship[d].get_height()//2
            msl_a[msl_id] = 270 #設定子彈的角度，270為向上飛行
            msl_id = (msl_id+1)%MSL_MAX #更新索引值
    if typ == 10:
        for a in range(160, 390, 10):
            msl_f[msl_id] = True
            msl_x[msl_id] = x
            msl_y[msl_id] = y-img_sship[d].get_height()//2
            msl_a[msl_id] = a
            msl_id = (msl_id+1)%MSL_MAX


def move_missile(scrn: pygame.Surface):
    global msl_f, msl_y
    for id in range(MSL_MAX):
        if msl_f[id]:
            # sin 以及 cos 讓我們知道在直角三角形不同的角度中，斜邊比底邊或是對邊的比值是多少，藉此算出位移
            msl_x[id] += 36*math.cos(math.radians(msl_a[id])) #利用 cos 方法取得速度在該角度可以取得的 x軸 份量，不會大於零（當角度是270度或是90度時cos為0）
            msl_y[id] += 36*math.sin(math.radians(msl_a[id])) #利用 sin 方法取得速度在該角度可以取得的 y軸 份量，不會大於零
            img_rz = pygame.transform.rotozoom(img_weapon, -90-msl_a[id], 1.0)
            scrn.blit(img_rz, [msl_x[id]-img_rz.get_width()//2, msl_y[id]-img_rz.get_height()//2])
            if msl_y[id] > SCREEN_Y or msl_y[id] < 0 or msl_x[id] > SCREEN_X or msl_x[id] < 0:
                msl_f[id] = False       


def bring_enemy():
    global tmr

    # 自動化出現敵機
    sec = tmr/FPS
    if tmr%int((FPS/(PLAYER+mode_number+1))) == 0:
        if 0 < sec < 15:
            set_enemy(random.randint(20, SCREEN_X-20), LINE_T, 90, ENEMY_TYPE, speed, 1)
        if 15 < sec < 30:
            set_enemy(random.randint(20, SCREEN_X-20), LINE_T, 90, ENEMY_TYPE+1, speed*2, 1)
            set_enemy(random.randint(20, SCREEN_X-20), LINE_T, 90, ENEMY_TYPE+1, speed*2, 1)
        if 30 < sec < 45:
            set_enemy(random.randint(20, SCREEN_X-20), LINE_T, random.randint(60, 120), ENEMY_TYPE+2, speed/2, (mode_number+1)*2)
        if 45 < sec < 60:
            set_enemy(random.randint(20, SCREEN_X-20), LINE_T, 90, ENEMY_TYPE+3, speed, mode_number+1)
    if tmr == 65*FPS:
        set_enemy(random.randint(20, SCREEN_X-20), LINE_T, 90, ENEMY_BOSS, 10+mode_number, PLAYER*100+mode_number*50)
    

def set_enemy(x, y, a, ty, sp, sh):
    for id in range(ENEMY_MAX):
        if emy_f[id] == False:
            emy_x[id] = x
            emy_y[id] = y
            emy_a[id] = a
            emy_type[id] = ty
            emy_speed[id] = sp
            emy_f[id] = True
            emy_shield[id] = sh
            emy_count[id] = 0
            break


def move_enemy(scrn: pygame.Surface):
    global ss_shield
    global idx, tmr, score
    global dis

    for id in range(ENEMY_MAX):
        if emy_f[id]:
            if emy_type[id] not in (ENEMY_BOSS, ENEMY_BOSS+1): #管理普通敵機的移動

                # 管理移動
                emy_x[id] += emy_speed[id]*math.cos(math.radians(emy_a[id]))
                emy_y[id] += emy_speed[id]*math.sin(math.radians(emy_a[id]))

                if emy_type[id] == 4:
                    emy_count[id] += 1
                    if emy_y[id] > 240 and emy_a[id] == 90: #當飛到一定低點後就隨機往個方向移動
                        emy_a[id] = random.choice([50, 70, 110, 130])
                        set_enemy(emy_x[id], emy_y[id], 90, EMY_BULLET, 10, 0)

                if emy_type[id] == 1 and emy_y[id] > 360:
                    if tmr%2 == 0:
                        set_enemy(emy_x[id], emy_y[id], 90, EMY_BULLET, 10, 0) #發射子彈
                    emy_a[id] = -45 #改變方向，左上
                    emy_speed[id] = 16

                # 管理敵機是否超越邊界
                if not LINE_L < emy_x[id] < LINE_R or not LINE_T < emy_y[id] < LINE_B: #當超越邊界時
                    emy_f[id] = False #設敵機不存在
            
            else: #管理魔王機的移動
                if emy_type[id] == ENEMY_BOSS+1: emy_type[id] = ENEMY_BOSS

                if emy_count[id] == 0:
                    emy_y[id] += emy_speed[id]
                    if emy_y[id] >= 200:
                        emy_count[id] = 1
                elif emy_count[id] == 1:
                    emy_x[id] -= emy_speed[id]
                    if emy_x[id] < 200:
                        emy_count[id] = 2
                        for j in range(20):
                            set_enemy(emy_x[id], emy_y[id]+80, 90-j/2*8, EMY_BULLET, speed, 0)
                    if tmr%abs((mode_number*5)-20) == 0:
                        set_enemy(emy_x[id], emy_y[id], random.randint(-20, 50), EMY_BULLET, speed, 0)
                elif emy_count[id] == 2:
                    emy_x[id] += emy_speed[id]
                    if emy_x[id] >= SCREEN_X-200:
                        emy_count[id] = 1
                        for j in range(20):
                            set_enemy(emy_x[id], emy_y[id]+80, 90+j/2*8, EMY_BULLET, speed, 0)
                    if tmr%abs((mode_number*5)-20) == 0:
                        set_enemy(emy_x[id], emy_y[id], random.randint(120, 200), EMY_BULLET, speed, 0)
                elif emy_count[id] == 3:
                    emy_x[id] += dis
                    if abs(emy_x[id] - SCREEN_X // 2) < abs(dis):  # 當接近中心點時更新狀態
                        emy_x[id] = SCREEN_X // 2  # 強制修正到中心點
                        emy_count[id] = 4
                elif emy_count[id] == 4:
                    if tmr%(int(FPS/(mode_number+1))) == 0:
                        for a in range(10, 170, 10):
                            set_enemy(emy_x[id], emy_y[id]+80, a, EMY_BULLET, speed, 0)
                        emy_count[id] = 5
                    if tmr%(FPS*2) == 0:
                        emy_count[id] = 5
                elif emy_count[id] == 5:
                    if tmr%1 == 0:
                        #計算角度
                        set_enemy(emy_x[id], emy_y[id]+80, tmr%16*10, EMY_BULLET, speed, 0)
                    if tmr%(FPS*3) == 0:
                        emy_count[id] = 6
                elif emy_count[id] == 6:
                    if tmr%1 == 0:
                        #計算角度
                        set_enemy(emy_x[id], emy_y[id]+80, abs(tmr%16-16)*10, EMY_BULLET, speed, 0)
                    if tmr%(FPS*3) == 0:
                        emy_count[id] = 5
                        
                if emy_count[id] < 4:
                    if tmr%(FPS/((mode_number+1)*2)) == 0:
                        set_enemy(emy_x[id], emy_y[id]+80, 90, EMY_BULLET, speed, 0)
                
                if emy_shield[id] < (PLAYER*100+mode_number*50)*0.25 and dis == 0: #當血量只剩下四分之一時
                    dis = int(SCREEN_X//2-emy_x[id])/20
                    emy_count[id] = 3
                            
            # 管理被擊落
            if emy_type[id] != EMY_BULLET: #當不是敵機子彈時
                w = img_enemy[emy_type[id]].get_width()
                h = img_enemy[emy_type[id]].get_height()
                r = int((w+h)/4)+12 #計算碰撞的距離，比實際的還要小
                er = int((w+h)/4) #處理爆炸特效的範圍
                for mi in range(MSL_MAX):
                    if msl_f[mi] == True and get_dis(emy_x[id], emy_y[id], msl_x[mi], msl_y[mi]) < r*r: #當有飛彈並且子彈與敵機的距離小於碰撞的距離時
                        emy_shield[id] -= 1
                        msl_f[mi] = False #刪除飛彈
                        set_effect(emy_x[id]+random.randint(-er, er), emy_y[id]+random.randint(-er, er)) #初始化爆炸特效

                        if emy_type[id] == ENEMY_BOSS: #如果是魔王機時
                            emy_type[id] = ENEMY_BOSS+1

                        if emy_shield[id] == 0: #當血量等於零的話
                            if emy_type[id] not in (ENEMY_BOSS, ENEMY_BOSS+1):
                                emy_f[id] = False #刪除敵機
                                score += (mode_number+1)*100 #加的分數會因為難度而提升
                                if ss_shield < 100:
                                    ss_shield += 1 #我機防禦率加一
                            else:
                                score += (mode_number+1)*10000
                                se_explosion.play()    
                                idx = 3
                                tmr = 0

            # 旋轉並繪製圖像
            ang = -90-emy_a[id] #計算畫面中旋轉的角度
            image = img_enemy[emy_type[id]] #儲存圖片
            img_rz = pygame.transform.rotozoom(image, ang, 1.0)
            scrn.blit(img_rz, [emy_x[id]-img_rz.get_width()//2, emy_y[id]-img_rz.get_height()//2])
            if emy_type[id] in (ENEMY_BOSS, ENEMY_BOSS+1):
                scrn.blit(img_shield, [emy_x[id]-img_shield.get_width()//2, emy_y[id]-img_enemy[emy_type[id]].get_height()//4-img_shield.get_height()])
                pygame.draw.rect(scrn, (64, 32, 32), [
                    emy_x[id] - img_shield.get_width() // 2 + (emy_shield[id] / (PLAYER * 100 + mode_number * 50))*400,
                    emy_y[id] - img_enemy[emy_type[id]].get_height() // 4 - img_shield.get_height(),
                    ((100 * PLAYER + 50 * mode_number) - emy_shield[id]) / (100 * PLAYER + 50 * mode_number) * 400,
                    12
                ])


def get_dis(x1, y1, x2, y2):
    return ((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)) #計算出兩個角色距離的平方


def draw_text(scrn: pygame.Surface, txt, x, y, siz, col, good: bool):
    fnt = pygame.font.Font(None, siz)
    sur = fnt.render(txt, True, col)

    # 根據中心點推導出右上角，如果 good 傳入 True 的話則直接是右上角
    if not good:
        x -= sur.get_width()//2
        y -= sur.get_height()//2

    scrn.blit(sur, [x, y])


def set_effect(x, y):
    global eff_id, eff_p, eff_x, eff_y, eff_id
    if eff_p[eff_id] == 0: #如果還沒有爆炸特效的話
        eff_p[eff_id] = 1
        eff_x[eff_id] = x
        eff_y[eff_id] = y
        eff_id = (eff_id+1)%EFFECT_MAX #管理 eff_id 的索引值


def draw_effect(scrn: pygame.Surface):
    global eff_p
    for id in range(EFFECT_MAX):
        if eff_p[id] != 0: #如果有設定爆炸特效的話
            scrn.blit(img_explore[eff_p[id]], [eff_x[id]-img_explore[eff_p[id]].get_width()//2, eff_y[id]-img_explore[eff_p[id]].get_height()//2]) #繪製爆炸特效
            eff_p[id] += 1
            if eff_p[id] == 6: #如果爆炸特效超過索引值的話
                eff_p[id] = 0


def main(): # 主要迴圈
    global ss_x, ss_y, ss_d, ss_shield, ss_invincible, score
    global bg_y, idx, tmr, speed, mode_number, Key_Down, Key_Up, player_speed
    global se_explosion, se_barrage, se_damage, se_shot

    pygame.init()
    pygame.display.set_caption("Galaxy Lancer")
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    clock = pygame.time.Clock()

    se_barrage = pygame.mixer.Sound("source/sound_gl/barrage.ogg")
    se_explosion = pygame.mixer.Sound("source/sound_gl/explosion.ogg")
    se_damage = pygame.mixer.Sound("source/sound_gl/damage.ogg")
    se_shot = pygame.mixer.Sound("source/sound_gl/shot.ogg")

    while True:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_F1 or event.key == K_LSHIFT:
                        screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), pygame.FULLSCREEN)
                    if event.key == K_F2 or event.key == K_RSHIFT:
                        screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
                if event.type == pygame.JOYDEVICEADDED:
                    joy = pygame.joystick.Joystick(event.device_index)
                    joysticks.append(joy)
        except Exception as error:
            print(error)

        # 時序
        tmr += 1

        # 捲動背景
        bg_y = (bg_y+speed)%SCREEN_Y
        for x in range(0, SCREEN_X, 960):
            screen.blit(img_galaxy, [x, bg_y-SCREEN_Y])
            screen.blit(img_galaxy, [x, bg_y])

        # 支援遊戲控制器
        try:
            while len(joysticks) < PLAYER:
                pygame.time.wait(500)
                print("沒有足夠的搖桿")
                pygame.quit()
                sys.exit()
            
            for id in range(PLAYER):
                axis0[id] = joysticks[id].get_axis(0)
                axis1[id] = joysticks[id].get_axis(1)
                BTright[id] = joysticks[id].get_button(0)
                BTdown[id] = joysticks[id].get_button(1)
                BTup[id] = joysticks[id].get_button(2)
                BTleft[id] = joysticks[id].get_button(3)

        except pygame.error as e:
            print(f"Joystick error: {e}")

        if idx == -1:
            if tmr == 1:
                speed = 5

            Key_Down = (Key_Down+1) * BTdown[0]
            Key_Up = (Key_Up+1) * BTup[0]

            if Key_Down == 1: #當下鍵被按下時
                mode_number += 1
                if mode_number == len(MODE):
                    mode_number = len(MODE)-1
            if Key_Up == 1:
                mode_number -= 1
                if mode_number < 0:
                    mode_number = 0
            if BTright[0] == True:
                if mode_number == 0:
                    player_speed = 25
                    speed = 10
                if mode_number == 1:
                    player_speed = 22
                    speed = 13
                if mode_number == 2:
                    player_speed = 19
                    speed = 16
                if mode_number == 3:
                    player_speed = 16
                    speed = 22

                idx = 0
                tmr = 0
                 
            draw_text(screen, "CHOOSE MODE", SCREEN_X//2, 75, 100, SILVER, False)
            for id, mode in enumerate(MODE):
                if mode_number != id: #當還沒有被選到時
                    draw_text(screen, mode, SCREEN_X//2, SCREEN_Y/(len(MODE)+1)*(id+1), 75, SILVER, False)
                else:
                    if tmr%10 < 5: #閃爍效果
                        draw_text(screen, mode, SCREEN_X//2, SCREEN_Y/(len(MODE)+1)*(id+1), 75, RED, False)
                
        if idx == 0:
            img_rz = pygame.transform.rotozoom(img_title[0], -tmr%360, 1) #逆時針旋轉漩渦
            screen.blit(img_rz, [SCREEN_X//2-img_rz.get_width()//2, SCREEN_Y*0.3-img_rz.get_height()//2]) #根據中心點推導出右上角
            screen.blit(img_title[1], [SCREEN_X//2-img_title[1].get_width()//2, SCREEN_Y*0.2])
            draw_text(screen, "PRESS [SPACE] TO START", SCREEN_X//2, SCREEN_Y*0.7, 50, SILVER, False)
            if tmr == 1:
                # 設定播放音樂
                pygame.mixer.music.load("source/sound_gl/bgm.ogg")
                pygame.mixer.music.play(-1)

            if tmr > FPS*2:
                if BTright[0] == 1: #當下
                    idx = 1
                    tmr = 0
                    score = 0

                    ss_shield = 100
                    for id in range(PLAYER):
                        ss_x[id] = 300+50*id
                        ss_y[id] = 600
                        ss_invincible[id] = 0

                    for id in range(ENEMY_MAX): emy_f[id] = False
                    for id in range(EFFECT_MAX): eff_p[id] = 0
                    for id in range(MSL_MAX): msl_f[id] = False



        if idx == 1:
            # 飛船
            move_starship(screen)
            # 子彈（等KEY接收到之後）
            move_missile(screen)
            # 敵人
            bring_enemy() #處理自動生成的敵人的函式
            move_enemy(screen)
        
        if idx == 2:
            move_missile(screen)
            move_enemy(screen) 
            if tmr == 1:
                pygame.mixer.music.stop()
            if tmr <= 90:
                if tmr%5 == 0:
                    for id in range(PLAYER):
                        set_effect(ss_x[id]+random.randint(-60, 60), ss_y[id]+random.randint(-60, 60))
                if tmr%10 == 0:
                    se_damage.play()
            if tmr == 120:
                pygame.mixer.music.load("source/sound_gl/gameover.ogg")
                pygame.mixer.music.play(0)
            if tmr > 120:
                draw_text(screen, "GAME OVER", screen.get_width()//2, screen.get_height()//2, 80, RED, False)
            if tmr == FPS*10:
                idx = 0
                tmr = 0
        
        if idx == 3:
            move_starship(screen) #繼續移動來嘲諷敵機
            move_missile(screen)
            if tmr == 1:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("source/sound_gl/gameclear.ogg")
            if tmr <= 90:
                if tmr%5 == 0:
                    for id in range(ENEMY_MAX): 
                        if emy_f[id] == True and emy_type[id] != EMY_BULLET: 
                            for _ in range(int(EFFECT_MAX/2)):
                                set_effect(
                                    random.randint(
                                        int(emy_x[id] - img_enemy[emy_type[id]].get_width() // 2),
                                        int(emy_x[id] + img_enemy[emy_type[id]].get_width() // 2)
                                    ),
                                    random.randint(
                                        int(emy_y[id] - img_enemy[emy_type[id]].get_height() // 2),
                                        int(emy_y[id] + img_enemy[emy_type[id]].get_height() // 2)
                                    )
                                )
                if tmr%10 == 0:
                    se_damage.play()
            if tmr == 90: pygame.mixer.music.play(0)
            if tmr >= 90: draw_text(screen, "GAME CLEAR!!!", screen.get_width()//2, screen.get_height()//2, 80, SILVER, False)
            if tmr == FPS*10:
                idx = 0
                tmr = 0

        # 爆炸動畫
        draw_effect(screen)

        draw_text(screen, "SCORE: "+str(score), 10, 20, 50, SILVER, True) #繪製分數
        
        if idx != 0:
            screen.blit(img_shield, [40, SCREEN_Y-40])
            pygame.draw.rect(screen, (64, 32, 32), [40+ss_shield*4, SCREEN_Y-40, (100-ss_shield)*4, 12])

        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
