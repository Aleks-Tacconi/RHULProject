from simplegui import GUI

WIDTH = 800
HEIGHT = 800
TITLE = "Game"


def main() -> None:
    my_gui = GUI(TITLE, WIDTH, HEIGHT)
    my_gui.start()

if __name__ == "__main__":
    main()
