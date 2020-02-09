import pyxel
import random
import time
import math

import Enemy as enemy
import Vector2 as vec2
import Player as pc
import Bullet as bullet
import Collide
import Particle as ptcl

WINDOW_H = 120
WINDOW_W = 200
PC_H = 16
PC_W = 8
ENEMY_H = 16
ENEMY_W = 16
STAGE_RIGHT = 190  # ステージの右端
STAGE_LEFT = 5
STAGE_TOP = 5
STAGE_BOTTOM = 93
ENEMIS_TOTAL = 8


class App:
    def __init__(self):
        pyxel.init(WINDOW_W, WINDOW_H, caption="Boss")
        pyxel.load("assets/Boss.pyxres")

        self.player_x = 100
        self.player_y = 100
        self.player_hp = 10
        self.enemy_hp = 100

        self.is_OP = True
        self.is_game_over = False
        self.is_game_clear = False

        # make instance
        self.pc = pc.pc()
        self.Balls = []
        self.Enemies = []
        self.Particles = []
        self.enemy_core = enemy.Enemy()

        pyxel.run(self.update, self.draw)

    def ctrl_enemy(self):
        # ====== ctrl enemy ====== #
        # enemy_coreの移動
        if pyxel.frame_count > 1500:
            self.enemy_core.update((math.sin(pyxel.frame_count/30))
                                   * 30 + 75, (math.cos(pyxel.frame_count/30)) * 30 + 60)
        elif pyxel.frame_count > 1000:
            self.enemy_core.update(
                abs(math.sin(pyxel.frame_count/50)) * 140, 20)
        elif pyxel.frame_count > 500:
            self.enemy_core.update(
                60, abs(math.sin(pyxel.frame_count/50)) * 100)
        elif pyxel.frame_count > 0:
            self.enemy_core.update(abs(math.cos(
                pyxel.frame_count/50)) * 100, abs(math.sin(pyxel.frame_count/50)) * 100)

        # 周りの匹の敵キャラを実体化
        if len(self.Enemies) <= ENEMIS_TOTAL:
            new_enemy = enemy.Enemy()
            new_enemy.update(self.enemy_core.pos.x*(math.sin(pyxel.frame_count/30)),
                             self.enemy_core.pos.y*(math.cos(pyxel.frame_count/30)))
            self.Enemies.append(new_enemy)

        enemy_count = len(self.Enemies)
        for i in range(enemy_count):
            # 当たり判定
            if ((self.pc.pos.x < self.Enemies[i].pos.x + ENEMY_W)
                and (self.Enemies[i].pos.x + ENEMY_W < self.pc.pos.x + PC_W)
                and (self.pc.pos.y < self.Enemies[i].pos.y + ENEMY_H)
                    and (self.Enemies[i].pos.y + ENEMY_H < self.pc.pos.y + PC_H)):
                self.player_hp -= 1

            # enemies動き
            self.Enemies[i].update((math.sin(pyxel.frame_count/30 * i)) * (30*(math.sin(pyxel.frame_count/50))) + self.enemy_core.pos.x,
                                   (math.cos(pyxel.frame_count/30 * i)) * (30 *
                                                                           (math.sin(pyxel.frame_count/50))) + self.enemy_core.pos.y)

    def ctrl_ball(self):
        # ====== ctrl Ball ======
        if pyxel.btnp(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD_1_A):
            new_ball = bullet.Bullet()
            if self.pc.direction == 3:
                new_ball.update(self.pc.pos.x + PC_W/2 - 6,
                                self.pc.pos.y + PC_H/2,
                                self.pc.vec, new_ball.size, new_ball.color)
                new_ball.direction = 3
            if self.pc.direction == 4:
                new_ball.update(self.pc.pos.x + PC_W/2 + 6,
                                self.pc.pos.y + PC_H/2,
                                self.pc.vec, new_ball.size, new_ball.color)
                new_ball.direction = 4
            if self.pc.direction == 5:
                new_ball.update(self.pc.pos.x + PC_W/2,
                                self.pc.pos.y + PC_H/2 - 6,
                                self.pc.vec, new_ball.size, new_ball.color)
                new_ball.direction = 5
            self.Balls.append(new_ball)

        ball_count = len(self.Balls)
        for i in range(ball_count):
            if 0 < self.Balls[i].pos.x and self.Balls[i].pos.x < WINDOW_W:
                # Ball update
                if self.Balls[i].direction == 3:
                    self.Balls[i].update(self.Balls[i].pos.x + self.Balls[i].speed,
                                         self.Balls[i].pos.y,
                                         self.Balls[i].vec, self.Balls[i].size, self.Balls[i].color)
                if self.Balls[i].direction == 4:
                    self.Balls[i].update(self.Balls[i].pos.x - self.Balls[i].speed,
                                         self.Balls[i].pos.y,
                                         self.Balls[i].vec, self.Balls[i].size, self.Balls[i].color)
                if self.Balls[i].direction == 5:
                    self.Balls[i].update(self.Balls[i].pos.x,
                                         self.Balls[i].pos.y -
                                         self.Balls[i].speed,
                                         self.Balls[i].vec, self.Balls[i].size, self.Balls[i].color)
              #  当たり判定(敵キャラとボール)
                enemy_count = len(self.Enemies)
                for j in range(enemy_count):
                    if ((self.Enemies[j].pos.x < self.Balls[i].pos.x)
                        and (self.Balls[i].pos.x < self.Enemies[j].pos.x + ENEMY_W)
                        and (self.Enemies[j].pos.y < self.Balls[i].pos.y)
                            and (self.Balls[i].pos.y < self.Enemies[j].pos.y + ENEMY_H)):
                        # 消滅(敵インスタンス破棄)
                        # enemyは体力性にする
                        self.enemy_hp -= 0
                        # パーティクル生成
                        for i in range(random.randint(1, 5)):
                            new_particle = ptcl.Ptcl(
                                self.Enemies[j].pos.x, self.Enemies[j].pos.y)
                            self.Particles.append(new_particle)
                        del self.Enemies[j]
                        break
            else:
                del self.Balls[i]
                break

    def ctrl_pc(self):
        # ====== ctrl pc ======
        dx = self.player_x - self.pc.pos.x  # x軸方向の移動量
        dy = self.player_y - self.pc.pos.y  # y軸方向の移動量

        if pyxel.btn(pyxel.KEY_B) or pyxel.btn(pyxel.GAMEPAD_1_B):  # JUMP
            self.player_y = max(self.player_y - 5, STAGE_TOP)
            self.pc.direction = 1

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):  # DOWN
            self.pc.direction = 2

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):  # MOVE RIGHT
            self.player_x = min(self.player_x + 4, STAGE_RIGHT)
            self.pc.direction = 3

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):  # MOVE LEFT
            self.player_x = max(self.player_x - 4, STAGE_LEFT)
            self.pc.direction = 4

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP):  # FACE UP
            self.pc.direction = 5

        if dx != 0:
            self.pc.update(self.player_x, self.player_y, dx)  # 座標と向きを更新
        elif dy != 0:
            self.pc.update(self.player_x, self.player_y,
                           self.pc.vec)  # 座標のみ更新（真上or真下に移動）

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.is_OP:
            if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD_1_A):
                self.is_OP = False
            return

        if self.is_game_over or self.is_game_clear:
            if pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.GAMEPAD_1_A):
                pyxel.quit()
            if pyxel.btn(pyxel.KEY_R):
                return
                # TODO リトライ機能の実装

        if self.player_hp < 0:
            self.is_game_over = True

        if self.enemy_hp < 0:
            self.is_game_clear = True

        self.pc.pos.x = self.player_x
        self.pc.pos.y = self.player_y

        # player.yの最小値
        self.player_y = min(self.player_y + 2, STAGE_BOTTOM)

        for i in range(len(self.Particles)):
            self.Particles[i].update()
   #         if self.Particles[i].life == 0:
            #  del self.Particles[i]

        self.ctrl_enemy()
        self.ctrl_ball()
        self.ctrl_pc()

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

        pyxel.cls(7)

        # ======= draw pc ========
        if self.pc.direction == 0:
            pyxel.blt(self.pc.pos.x, self.pc.pos.y, 0, 0, 0, 16, 16, 1)
        if self.pc.direction == 1:
            pyxel.blt(self.pc.pos.x, self.pc.pos.y, 0, 0, 0, 16, 16, 1)
        if self.pc.direction == 2:
            pyxel.blt(self.pc.pos.x, self.pc.pos.y, 0, 0, 48, 16, 16, 1)
        if self.pc.direction == 3:
            pyxel.blt(self.pc.pos.x, self.pc.pos.y, 0, 0, 16, 16, 16, 1)
        if self.pc.direction == 4:
            pyxel.blt(self.pc.pos.x, self.pc.pos.y, 0, 0, 32, 16, 16, 1)
        if self.pc.direction == 5:
            pyxel.blt(self.pc.pos.x, self.pc.pos.y, 0, 0, 0, 16, 16, 1)

        # ====== draw Balls ======
        for ball in self.Balls:
            pyxel.circ(ball.pos.x, ball.pos.y, ball.size, ball.color)

        # ====== draw Patrticle =====#
        for particle in self.Particles:
            pyxel.circ(particle.pos.x, particle.pos.y, particle.r, 3)
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
        pyxel.text(30, 110, "E", 8)
        for i in range(self.enemy_hp):
            pyxel.line(40+i*2, 110, 40+i*2, 113, 8)

    def draw_OP(self):
        pyxel.cls(5)
        pyxel.text(60, 60, "START", 1)
        pyxel.text(59, 60, "START", 7)

    def draw_clear_screen(self):
        pyxel.text(60, 60, "FINISH", 1)
        pyxel.text(59, 60, "FINISH", 7)

    def draw_crash_screen(self):
        pyxel.text(50, 60, "GAME OVER", random.randint(1, 15))
        pyxel.text(49, 60, "GAME OVER", 0)


App()
