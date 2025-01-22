from .entity import Entity
from .animation import Animation


class Player(Entity):
    def __init__(self, game):
        super().__init__(pos=[150, 150], size=[400, 400])

        self.game = game
        self.speed = 4

        self.current_animation = "idle"
        self.animations = {
            "idle": Animation("assets/player/IDLE.png", 1, 5, 15),
            "run right": Animation("assets/player/RUN.png", 1, 8, 15),
            "run left": Animation("assets/player/RUN.png", 1, 8, 15, flipped=True),
        }

    def render(self, canvas):
        self.animations[self.current_animation].render(canvas, self.pos, self.size)

    def update(self):
        self.animations[self.current_animation].update()

        if ("A" in self.game.keys_pressed and "D" in self.game.keys_pressed) or \
            ("A" not in self.game.keys_pressed and "D" not in self.game.keys_pressed):
            self.current_animation = "idle"
        elif "A" in self.game.keys_pressed:
            self.pos[0] -= self.speed
            self.current_animation = "run left"
        elif "D" in self.game.keys_pressed:
            self.pos[0] += self.speed
            self.current_animation = "run right"
