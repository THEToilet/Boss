class EnemyMove:
    def move_circle(self):
        self.enemy_core.update((math.sin(pyxel.frame_count/30))
                               * 30 + 75, (math.cos(pyxel.frame_count/30)) * 30 + 60)
