import pyxel
import random

WINDOW_H = 120
WINDOW_W = 150
PC_H = 16
PC_W = 16
ENEMY_H = 16
ENEMY_W = 16


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class pc:
    def __init__(self):
        self.pos = Vec2(10, 95)
        self.vec = 0

    def update(self, x, y, dx):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx


class Ball:
    def __init__(self):
        self.pos = Vec2(0, 0)
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


class Enemy:
    def __init__(self):
        self.pos = Vec2(0, 0)
        self.vec = 0
        self.speed = 0.02

    def update(self, x, y, dx):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx


class App:
    def __init__(self):
        self.player_x = 0
        self.player_y = 0
        self.player_hp = 30
        self.enemy_hp = 30
        pyxel.init(WINDOW_W, WINDOW_H, caption="kamisama")
        pyxel.load("kami.pyxel")

        self.is_OP = True
        self.is_game_over = False
        self.is_game_clear = False

        # make instance
        self.mpc = pc()
        self.Balls = []
        self.Enemies = []
        self.lasers = []

        # flag
        self.flag = 3
        self.GameOver_flag = 0

        #
        self.player_x = self.mpc.pos.x
        self.player_y = self.mpc.pos.y
        self.mpc.pos.x = self.mpc.pos.x
        self.mpc.pos.y = self.mpc.pos.y

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_R):
            self.score = 0
            self.__init__()

        if self.player_hp == 0:
            self.is_game_over = True

        if self.enemy_hp == 0:
            self.is_game_clear = True

        if self.is_OP:
            if pyxel.btn(pyxel.constants.KEY_S):
                self.is_OP = False
            return

        if self.is_game_over or self.is_game_clear:
            if pyxel.btn(pyxel.constants.KEY_Q):
                pyxel.quit()
            if pyxel.btn(pyxel.constants.KEY_R):
                self.__init__()
            return
        self.mpc.pos.x = self.player_x
        self.mpc.pos.y = self.player_y

        self.player_y = min(self.player_y + 4, 95)
        # ====== ctrl pc ======
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
            self.player_x = max(self.player_x - 4, 5)

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
            self.player_x = min(self.player_x + 4, 130)

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP):
            self.player_y = max(self.player_y - 12, 5)

        dx = self.player_x - self.mpc.pos.x  # x軸方向の移動量(マウス座標 - cat座標)
        dy = self.player_y - self.mpc.pos.y  # y軸方向の移動量(マウス座標 - cat座標)

        if dx != 0:
            self.mpc.update(self.player_x, self.player_y, dx)  # 座標と向きを更新
        elif dy != 0:
            self.mpc.update(self.player_x, self.player_y,
                            self.mpc.vec)  # 座標のみ更新（真上or真下に移動）

        # ====== ctrl enemy ======

        if self.flag > 0:  # 1匹の敵キャラを実体化
            new_enemy = Enemy()
            new_enemy.update(random.randrange(WINDOW_W),
                             random.randrange(WINDOW_H), self.mpc.vec)
            self.Enemies.append(new_enemy)

            self.flag -= 1

        enemy_count = len(self.Enemies)
        for i in range(enemy_count):
            # 当たり判定(敵キャラと猫)
            if ((self.mpc.pos.x < self.Enemies[i].pos.x + ENEMY_W)
                and (self.Enemies[i].pos.x + ENEMY_W < self.mpc.pos.x + PC_W)
                and (self.mpc.pos.y < self.Enemies[i].pos.y + ENEMY_H)
                    and (self.Enemies[i].pos.y + ENEMY_H < self.mpc.pos.y + PC_H)):
                self.player_hp -= 1

            # P制御
            ex = (self.mpc.pos.x - self.Enemies[i].pos.x)
            ey = (self.mpc.pos.y - self.Enemies[i].pos.y)
            Kp = self.Enemies[i].speed
            if ex != 0 or ey != 0:
                self.Enemies[i].update(self.Enemies[i].pos.x + ex * Kp,
                                       self.Enemies[i].pos.y + ey * Kp,
                                       self.mpc.vec)

        # ====== ctrl Ball ======
        if pyxel.btnp(pyxel.KEY_A):
            new_ball = Ball()
            if self.mpc.vec > 0:
                new_ball.update(self.mpc.pos.x + PC_W/2 + 6,
                                self.mpc.pos.y + PC_H/2,
                                self.mpc.vec, new_ball.size, new_ball.color)
            else:
                new_ball.update(self.mpc.pos.x + PC_W/2 - 6,
                                self.mpc.pos.y + PC_H/2,
                                self.mpc.vec, new_ball.size, new_ball.color)
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
                        del self.Enemies[j]
                        self.enemy_hp -= 2
                        self.flag = 1
                        break
            else:
                del self.Balls[i]
                break

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
      #  pyxel.text(55, 40, "Are you Kururu?", pyxel.frame_count % 16)
     #   pyxel.blt(self.IMG_ID0_X, self.IMG_ID0_Y, self.IMG_ID0, 0, 0, 38, 16)

        # ======= draw pc ========
        if self.mpc.vec > 0:
            pyxel.blt(self.mpc.pos.x, self.mpc.pos.y, 0, 0, 0, 16, 16, 1)
        else:
            pyxel.blt(self.mpc.pos.x, self.mpc.pos.y, 0, 0, 16, 16, 16, 1)

        # ====== draw Balls ======
        for ball in self.Balls:
            pyxel.circ(ball.pos.x, ball.pos.y, ball.size, ball.color)

        # ====== draw enemy ======
        for enemy in self.Enemies:
            #        print("a")
            if enemy.vec > 0:
             #           print("a")
                pyxel.blt(enemy.pos.x, enemy.pos.y, 0, 16, 0, 16, 16, 1)
            else:
                pyxel.blt(enemy.pos.x, enemy.pos.y, 0, 16, 0, 16, 16, 1)

        # draw_player_hp
        for i in range(self.player_hp):
            pyxel.line(5+i*2, 110, 5+i*2, 113, 10)

        # draw_enemy_hp
        for i in range(self.enemy_hp):
            pyxel.line(75+i*2, 110, 75+i*2, 113, 11)

        # ====== draw game over ======
        if self.GameOver_flag == 1:
            pyxel.text(self.mpc.pos.x - 10, self.mpc.pos.y - 5, "GAME OVER", 8)

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
