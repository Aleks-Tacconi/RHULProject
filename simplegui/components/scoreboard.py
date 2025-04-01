from collections import defaultdict

from entities.abstract import Entity


class ScoreBoard:
    def __init__(self) -> None:
        self.__count = 0
        self.__time = 0
        self.__base_score = 1000
        self.__scores = defaultdict()
        self.__scores["tutorial"] = 0
        self.__scores["LevelOne"] = 0
        self.__scores["LevelTwo"] = 0
        self.__scores["LevelThree"] = 0
        self.__enemy_killed_score = 0

    def update(self) -> None:
        if self.__count % 60 == 0:
            self.__time += 1

    def calculate_score(self, level: str) -> None:
        self.__scores[level] = (
            self.__base_score - min(self.__time, 1000) + self.__enemy_killed_score
        )

    def print_score(self) -> None:
        print(self.__scores)

    def enemy_killed_score(self, entity: Entity) -> None:
        if entity.give_points:
            entity.give_points = False
            self.__enemy_killed_score += entity.points

    def return_score(self, level: str) -> int:
        return self.__scores[level]
