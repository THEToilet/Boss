import pyxel
import random
import time
import math
import Enemy as enemy
import Vector2 as vec2

WINDOW_H = 120
WINDOW_W = 150
PC_H = 16
PC_W = 16
ENEMY_H = 16
ENEMY_W = 16


class pc:
    def __init__(self):
        self.pos = vec2.Vec2(10, 95)
        self.vec = 0

    def update(self, x, y, dx):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx


class Ball:
    def __init__(self):
        self.pos = vec2.Vec2(0, 0)
        self.vec = 0
        self.size = 2
        self.speed = 3
        self.color = 8  # 0~15

    def update(self, x, y, dx, size, color):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx
        self.size = size
        self.color = color


class App:
    def __init__(self):
        self.player_x = 100
        self.player_y = 100
        self.player_hp = 1
        self.enemy_hp = 40
        pyxel.init(WINDOW_W, WINDOW_H, caption="Boss")
        pyxel.load("assets/Boss.pyxres")

        self.is_OP = True
        self.is_game_over = False
        self.is_game_clear = False

        # make instance
        self.pc = pc()
        self.Balls = []
        self.Enemies = []
        self.lasers = []

        self.enemy_core = enemy.Enemy()

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_R):
            self.score = 0
            self.__init__()

        if self.player_hp < 0:
            self.is_game_over = True

        if self.enemy_hp < 0:
            self.is_game_clear = True

        if self.is_OP:
            if pyxel.btn(pyxel.KEY_S):
                self.is_OP = False
            return

        if self.is_game_over or self.is_game_clear:
            if pyxel.btn(pyxel.KEY_Q):
                pyxel.quit()
            if pyxel.btn(pyxel.KEY_R):
                self.__init__()
            return
        self.pc.pos.x = self.player_x
        self.pc.pos.y = self.player_y

        self.player_y = min(self.player_y + 4, 95)

        self.ctrl_enemy()
        self.ctrl_ball()
        self.ctrl_pc()

    def ctrl_enemy(self):
        # ====== ctrl enemy ======
        # enemy_coreの移動
        self.enemy_core.update(abs(math.sin(time.time()/2)) * 140, 20, 1)
       # print((abs(math.sin(time.time()))))

        # 1匹の敵キャラを実体化
        if len(self.Enemies) < 20:
            new_enemy = enemy.Enemy()
            new_enemy.update(random.randrange(WINDOW_W),
                             random.randrange(WINDOW_H), self.pc.vec)
            self.Enemies.append(new_enemy)

        enemy_count = len(self.Enemies)
        for i in range(enemy_count):
            # 当たり判定(敵キャラと猫)
            if ((self.pc.pos.x < self.Enemies[i].pos.x + ENEMY_W)
                and (self.Enemies[i].pos.x + ENEMY_W < self.pc.pos.x + PC_W)
                and (self.pc.pos.y < self.Enemies[i].pos.y + ENEMY_H)
                    and (self.Enemies[i].pos.y + ENEMY_H < self.pc.pos.y + PC_H)):
                self.player_hp -= 1

            # P制御
            ex = (self.enemy_core.pos.x - self.Enemies[i].pos.x)
            ey = (self.enemy_core.pos.y - self.Enemies[i].pos.y)
            Kp = self.Enemies[i].speed
            if ex != 0 or ey != 0:
                self.Enemies[i].update(self.Enemies[i].pos.x + ex * Kp,
                                       self.Enemies[i].pos.y + ey * Kp,
                                       self.pc.vec)

    def ctrl_ball(self):
        # ====== ctrl Ball ======
        if pyxel.btnp(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD_1_A):
            new_ball = Ball()
            if self.pc.vec > 0:
                new_ball.update(self.pc.pos.x + PC_W/2 + 6,
                                self.pc.pos.y + PC_H/2,
                                self.pc.vec, new_ball.size, new_ball.color)
            else:
                new_ball.update(self.pc.pos.x + PC_W/2 - 6,
                                self.pc.pos.y + PC_H/2,
                                self.pc.vec, new_ball.size, new_ball.color)
            self.Balls.append(new_ball)

        ball_count = len(self.Balls)
        for i in range(ball_count):
            if 0 < self.Balls[i].pos.x and self.Balls[i].pos.x < WINDOW_W:
                # Ball update
                if self.Balls[i].vec > 0:
                    self.Balls[i].update(self.Balls[i].pos.x + self.Balls[i].speed,
                                         self.Balls[i].pos.y,
                                         self.Balls[i].vec, self.Balls[i].size, self.Balls[i].color)
                else:
                    self.Balls[i].update(self.Balls[i].pos.x - self.Balls[i].speed,
                                         self.Balls[i].pos.y,
                                         self.Balls[i].vec, self.Balls[i].size, self.Balls[i].color)
              #  当たり判定(敵キャラとボール)
                enemy_count = len(self.Enemies)
                for j in range(enemy_count):
                    if ((self.Enemies[j].pos.x < self.Balls[i].pos.x)
                        and (self.Balls[i].pos.x < self.Enemies[j].pos.x + ENEMY_W)
                        and (self.Enemies[j].pos.y < self.Balls[i].pos.y)
                            and (self.Balls[i].pos.y < self.Enemies[j].pos.y + ENEMY_H)):
                        # 消滅(敵インスタンス破棄)
                      #  del self.Enemies[j] enemyは体力性にする
                        self.enemy_hp -= 2
                        self.flag = 1
                        break
            else:
                del self.Balls[i]
                break

    def ctrl_pc(self):
        # ====== ctrl pc ======
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
            self.player_x = max(self.player_x - 4, 5)

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
            self.player_x = min(self.player_x + 4, 130)

        if pyxel.btn(pyxel.KEY_B) or pyxel.btn(pyxel.GAMEPAD_1_B):
            self.player_y = max(self.player_y - 10, 5)

        dx = self.player_x - self.pc.pos.x  # x軸方向の移動量(マウス座標 - cat座標)
        dy = self.player_y - self.pc.pos.y  # y軸方向の移動量(マウス座標 - cat座標)

        if dx != 0:
            self.pc.update(self.player_x, self.player_y, dx)  # 座標と向きを更新
        elif dy != 0:
            self.pc.update(self.player_x, self.player_y,
                           self.pc.vec)  # 座標のみ更新（真上or真下に移動）

    def draw(self):
        if self.is_OP:
            self.draw_OP()
            return

        if self.is_game_over:
            self.draw_crash_screen()
            return

        if self.is_game_clear:
            self.draw_clear_screen()
            return

        pyxel.cls(0)

        # ======= draw pc ========
        if self.pc.vec > 0:
            pyxel.blt(self.pc.pos.x, self.pc.pos.y, 0, 0, 0, 16, 16, 1)
        else:
            pyxel.blt(self.pc.pos.x, self.pc.pos.y, 0, 0, 16, 16, 16, 1)

        # ====== draw Balls ======
        for ball in self.Balls:
            pyxel.circ(ball.pos.x, ball.pos.y, ball.size, ball.color)

        # ====== draw enemy ======
        for enemy in self.Enemies:
            if enemy.vec > 0:
                pyxel.blt(enemy.pos.x, enemy.pos.y, 0, 16, 0, 16, 16, 1)
            else:
                pyxel.blt(enemy.pos.x, enemy.pos.y, 0, 16, 0, 16, 16, 1)
        pyxel.blt(self.enemy_core.pos.x,
                  self.enemy_core.pos.y, 0, 32, 0, 16, 16, 1)

        # draw_player_hp
      #  for i in range(self.player_hp):
      #      pyxel.line(5+i*2, 110, 5+i*2, 113, 10)

        # draw_enemy_hp
        pyxel.text(30,110,"E",8)
        for i in range(self.enemy_hp):
            pyxel.line(40+i*2, 110, 40+i*2, 113, 8)

    def draw_OP(self):
        pyxel.cls(5)
        pyxel.text(60, 60, "START", 1)
        pyxel.text(59, 60, "START", 7)

    def draw_clear_screen(self):
        pyxel.cls(2)
        pyxel.text(60, 60, "FINISH", 1)
        pyxel.text(59, 60, "FINISH", 7)

    def draw_crash_screen(self):
        pyxel.cls(3)
        pyxel.text(50, 60, "GAME OVER", 1)
        pyxel.text(49, 60, "GAME OVER", 7)


App()
