import random
import math
import Vector2 as vec2


class Ptcl:
    def __init__(self, x, y):
        self.pos = vec2.Vec2(x, y)
        self.vx = math.sin(x)
        self.vy = math.cos(y)
        self.r = random.randint(0, 2)
        self.life = random.randint(1, 4)
        self.direction = 0

    def update(self):
        self.pos.x += self.vx
        self.pos.y += self.vy
        self.life -= 1
