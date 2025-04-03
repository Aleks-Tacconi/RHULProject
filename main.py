from simplegui import GUI

WIDTH = 800
HEIGHT = 400
TITLE = "Game"


def main() -> None:
    my_gui = GUI(TITLE, WIDTH, HEIGHT)
    my_gui.start()

if __name__ == "__main__":
    main()


"""
        if "V" in self.keyboard.keys_pressed and self.single == True:
             #Make it only call once + Threading (Will be done soon)
             self.single = False
             speech = self.ai.speak()
             print(speech)
             response = self.ai.text_prompt(speech + "\n\n" + "Act like a game tutorial assistant and address the player as the chosen one.")
             self.ai.generate_response_voice_backup(response)
             self.single = True
         print(self.single)
"""
