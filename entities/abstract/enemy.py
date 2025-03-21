from abc import ABCMeta, abstractmethod

from .physics_entity import PhysicsEntity


class Enemy(PhysicsEntity, metaclass=ABCMeta):
    @abstractmethod
    def interaction(self, entity: PhysicsEntity) -> None: ...
