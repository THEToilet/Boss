import random
import math
import Vector2 as vec2


class Ptcl:
    def __init__(self, x, y):
        self.pos = vec2.Vec2(x, y)
        self.vx = math.sin(x)
        self.vy = math.cos(y)
        self.r = random.randint(0, 2)
        self.life = random.randint(7, 9)
        self.direction = 0
        self.speed = 2

    def update(self):
        self.pos.x += self.vx * self.speed
        self.pos.y += self.vy * self.speed
        self.life -= 1
