import math


def distance(x1, y1, x2, y2):
   # print(math.sqrt(pow(x1-x2, 2)+pow(y1-y2, 2)))
    return math.sqrt(pow(x1-x2, 2)+pow(y1-y2, 2))


def collision(x1, y1, x2, y2, r):
    if distance(x1, y1, x2, y2) < r:
        return True
    else:
        return False


def collide_with_other_enemies(Enemies, enemy, r):  # r半径
    for i in range(len(Enemies)):
        if enemy != Enemies[i] and collision(enemy.pos.x, enemy.pos.y, Enemies[i].pos.x, Enemies[i].pos.y, r):
            return True
    return False
