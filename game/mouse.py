from vector import Vector

class Mouse:
    def __init__(self):
        self.mouse_position = Vector(0, 0)

    def mouse_click(self, position):
        self.mouse_position = Vector(position[0], position[1])
        print(self.mouse_position)
