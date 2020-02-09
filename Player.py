import Vector2 as vec2

class pc:
    def __init__(self):
        self.pos = vec2.Vec2(10, 95)
        self.vec = 0
        self.direction = 0
        self.is_floating = False

    def update(self, x, y, dx):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx