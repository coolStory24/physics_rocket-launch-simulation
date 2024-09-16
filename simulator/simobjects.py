import pygame
from pygame.sprite import Sprite

from config import MIN_PLANETARY_SIZE, MIN_ROCKET_SIZE
from entities import Planet, RoundRocket
from physics import Entity, Vector


class SimObject(Sprite):
    def __init__(self, entity: Entity, name: str=""):
        super().__init__()
        self.entity = entity
        self.name = name

    def draw(self, screen, scale: float, offset: Vector):
        raise NotImplementedError()


class SimPlanetaryObject(SimObject):
    def __init__(self, entity: Planet, color=pygame.Color("White"), name: str=""):
        super().__init__(entity, name=name)
        self.color = color

    def draw(self, screen, scale: float, offset: Vector):
        if not isinstance(self.entity, Planet):
            raise ValueError("Entity is not a Planet")
        pygame.draw.circle(
            screen, self.color,
            (self.entity.position.x * scale + offset.x, self.entity.position.y * scale + offset.y),
            max(int(self.entity.radius * scale), MIN_PLANETARY_SIZE)
        )


class SimRoundRocketObject(SimObject):
    def __init__(self, entity: RoundRocket, color=pygame.Color("firebrick1"), name: str = ""):
        super().__init__(entity, name=name)
        self.color = color

    def draw(self, screen, scale: float, offset: Vector):
        if not isinstance(self.entity, RoundRocket):
            print(self.entity.__class__)
            raise ValueError("Entity is not a Round Rocket")
        pygame.draw.circle(
            screen, self.color,
            (self.entity.position.x * scale + offset.x, self.entity.position.y * scale + offset.y),
            max(int(self.entity.radius * scale), MIN_ROCKET_SIZE)
        )
