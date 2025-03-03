class Keyboard:
    def __init__(self):
        self.keys_pressed = set()
        self.current_key = ""

    def keydown(self, key):
        try:
            self.keys_pressed.add(chr(key))
            if chr(key) in "AD":
                self.current_key = chr(key)
        except ValueError:
            pass

    def keyup(self, key):
        try:
            self.keys_pressed.remove(chr(key))
            self.current_key = ""
        except ValueError:
            pass

