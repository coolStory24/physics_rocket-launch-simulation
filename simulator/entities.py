import pygame
from pygame.sprite import Sprite

from physics import Entity, Point, Vector
from config import MIN_PLANETARY_SIZE


class Planet(Entity):
    def __init__(self, weight: float, position: Point, speed: Vector, radius: float):
        super().__init__(weight, position, speed)
        self.radius = radius


class SimObject(Sprite):
    def __init__(self, entity: Entity, name: str=""):
        super().__init__()
        self.entity = entity
        self.name = name

    def draw(self, screen, scale: float, offset: Vector):
        raise NotImplementedError()


class SimPlanetaryObject(SimObject):
    def __init__(self, entity: Entity, color=pygame.Color("White"), name: str=""):
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
