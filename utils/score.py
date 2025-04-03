import json
import os


class Score:
    def __init__(self) -> None:
        if not os.path.exists("scores.json"):
            with open(file="scores.json", mode="w+", encoding="utf-8") as f:
                f.write("{}")

        self.current_score = 0
        self.__user = ""

        self.scores = {}
        self.__load_scores()

    def new_user(self, username: str, passwd: str) -> None:
        self.scores[username] = {
            "score": 0,
            "password": passwd,
        }

        self.update_scores()

    def encrypt(self, passwd: str) -> str:
        return passwd

    def login(self, user: str, passwd: str) -> bool:
        encrypted = self.encrypt(passwd)

        if user not in self.scores:
            return False

        if self.scores[user]["password"] == encrypted:
            self.__user = user
            return True

        return False

    def add_score(self, score: int, boolean: bool) -> None:
        if boolean:
            self.current_score += score

        self.update()
        self.update_scores()

    def __load_scores(self) -> None:
        with open(file="scores.json", mode="r", encoding="utf-8") as f:
            self.scores = json.load(f)

    def update(self) -> None:
        if self.__user not in self.scores:
            return

        if self.current_score > self.scores[self.__user]["score"]:
            self.scores[self.__user]["score"] = self.current_score

    def update_scores(self) -> None:
        with open(file="scores.json", mode="w", encoding="utf-8") as f:
            json.dump(self.scores, f)


SCORE = Score()
