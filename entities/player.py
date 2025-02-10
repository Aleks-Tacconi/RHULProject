from .entity import Entity
from .animation import Animation
import os
from vector import Vector

class Player(Entity):
    def __init__(self, game):
        super().__init__(pos=Vector(150,150), size=[220, 220])
        self.game = game
        self.vel = Vector()
        self.current_animation = "idle"
        self.animations = {
            "idle": Animation(os.path.join("assets","player","IDLE.png"), 1, 5, 15),
            "run right": Animation(os.path.join("assets","player","RUN.png"), 1, 8, 15),
            "run left": Animation(os.path.join("assets","player","RUN.png"), 1, 8, 15,
                                  flipped=True),
            "jump": Animation(os.path.join("assets","player","JUMP.png"), 1, 3, 15)
        }

    def render(self, canvas):
        self.animations[self.current_animation].render(canvas, self.pos.get_p(), self.size)

    def update(self):
        self.animations[self.current_animation].update()

        if self.vel.x == 0:
            self.current_animation = "idle"
        if self.vel.x < 0:
            self.current_animation = "run left"
        if self.vel.x > 0:
            self.current_animation = "run right"
        if self.vel.y > 0:
            self.current_animation = "jump"

        self.pos.add(self.vel)
        self.gravity()

