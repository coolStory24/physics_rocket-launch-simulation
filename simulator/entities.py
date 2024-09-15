import pygame
from pygame.sprite import Sprite

from physics import Entity, Point, Vector


class Planet(Entity):
    def __init__(self, weight: float, position: Point, speed: Vector, radius: float):
        super().__init__(weight, position, speed)
        self.radius = radius

    def draw(self, screen, scale, offset: Vector):
        raise NotImplementedError()


class SimPlanetaryObject(Sprite):
    def __init__(self, entity: Entity, color=pygame.Color("White")):
        super().__init__()
        self.entity = entity
        self.color = color

    def draw(self, screen, scale, offset: Vector):
        if not isinstance(self.entity, Planet):
            raise ValueError("Entity is not a Planet")
        pygame.draw.circle(
            screen, self.color,
            (self.entity.position.x * scale + offset.x, self.entity.position.y * scale + offset.y),
            max(int(self.entity.radius * scale), 1)
        )
