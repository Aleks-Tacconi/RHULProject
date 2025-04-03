from collections import defaultdict

from entities.abstract import Entity, Enemy


class XP:
    def __init__(self) -> None:
        self.__count = 0
        self.__time = 0
        self.__xp = 0
        self.__xp = defaultdict()
        self.__xp["tutorial"] = 0
        self.__xp["LevelOne"] = 0
        self.__xp["LevelTwo"] = 0
        self.__xp["LevelThree"] = 0
        self.__enemy_killed_xp = 0

    def update(self) -> None:
        if self.__count % 60 == 0:
            self.__time += 1

    def print_xp(self) -> None:
        print(self.__xp)

    def enemy_killed_xp(self, entity: Entity, level: str) -> None:
        if entity.give_xp:
            entity.give_xp = False
            self.__xp[level] += entity.xp

    def return_xp(self, level: str) -> int:
        return self.__xp[level]
    
    def reset_xp(self, id: str) -> None:
        self.__xp[id] = 0
