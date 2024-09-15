import pygame
from pygame.sprite import Sprite, Group

from physics import Entity, Point, Vector, Physics


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

class PhysicsGroup(Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def update(self, delta_time: float):
        entities = [sprite.entity for sprite in self.sprites()]
        for i, entity in enumerate(entities):
            for other_entity in entities[i + 1:]:
                Physics.apply_gravity(entity, other_entity)
            Physics.move(entity, delta_time)

    def render(self, screen, scale):
        for entity in self.sprites():
            entity.draw(screen, scale)
