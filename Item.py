import Vector2 as vec2

class Enemy:
    def __init__(self):
        self.pos = vec2.Vec2(0, 0)
        self.vec = 0
        self.speed = 0.05
        self.category = ""

    def update(self, x, y):
        self.pos.x = x
        self.pos.y = y