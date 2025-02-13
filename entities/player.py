from .entity import Entity
from .animation import Animation
import os
from vector import Vector

class Player(Entity):
    def __init__(self, game):
        super().__init__(pos=Vector(150,150), size=[220, 220])
        self.game = game
        self.vel = Vector()
        self.current_animation = ""
        self.direction = ""
        self.animations = {
            "idle right": Animation(os.path.join("assets","player","IDLE.png"), 1, 5, 15),
            "idle left": Animation(os.path.join("assets","player","IDLE.png"), 1, 5, 15,
                                   flipped=True),
            "run right": Animation(os.path.join("assets","player","RUN.png"), 1, 8, 15),
            "run left": Animation(os.path.join("assets","player","RUN.png"), 1, 8, 15,
                                  flipped=True),
            "jump right": Animation(os.path.join("assets","player","JUMP.png"), 1, 3, 15),
            "jump left": Animation(os.path.join("assets","player","JUMP.png"), 1, 3, 15,
                                   flipped=True),
        }

    def render(self, canvas):
        self.animations[self.current_animation].render(canvas, self.pos.get_p(), self.size)

    def update(self):
        if self.direction == "":
            self.current_animation = "idle right"

        if self.vel.x != 0:
            if self.vel.x > 0:
                self.direction = "right"
            if self.vel.x < 0:
                self.direction = "left"

        if self.direction == "right":
            if self.vel == Vector(0,0):
                self.current_animation = "idle right"
            if self.vel.y != 0:
                self.current_animation = "jump right"

        if self.direction == "left":
            if self.vel == Vector(0, 0):
                self.current_animation = "idle left"
            if self.vel.y != 0:
                self.current_animation = "jump left"

        if self.vel.x > 0:
            self.current_animation = "run right"
        if self.vel.x < 0:
            self.current_animation = "run left"

        self.pos.add(self.vel)
        self.gravity()
        self.animations[self.current_animation].update()

