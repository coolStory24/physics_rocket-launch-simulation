import pygame
from pygame.sprite import Sprite

from physics import Entity, Point, Vector


class Planet(Entity):
    def __init__(self, weight: float, position: Point, speed: Vector, radius: float):
        super().__init__(weight, position, speed)
        self.radius = radius


class SimPlanetaryObject(Sprite):
    def __init__(self, entity: Entity, screen_coordinates, color=pygame.Color("White")):
        super().__init__()
        self.entity = entity
        self.x = screen_coordinates[0]
        self.y = screen_coordinates[1]
        self.color = color

    def draw(self, screen, scale):
        if not isinstance(self.entity, Planet):
            raise ValueError("Entity is not a Planet")
        pygame.draw.circle(screen, self.color, (self.x, self.y), int(self.entity.radius * scale))
