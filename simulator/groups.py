import pygame
import math

from pygame.sprite import Group, Sprite
from math import pi

import config
from physics import Vector, Physics
from simobjects import SimRocketObject, SimPlanetaryObject
from events import RocketEvent, EventRegistrer, CollisionEvent


class PhysicsGroup(Group):
    def __init__(self, *sprites: Sprite):
        super().__init__(*sprites)

    def update(self, delta_time: float):
        entities = [sprite.entity for sprite in self.sprites()]
        for entity in entities:
            entity.force = Vector((0, 0))


class GravityGroup(PhysicsGroup):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def update(self, delta_time: float):
        entities = [sprite.entity for sprite in self.sprites()]
        for i, entity in enumerate(entities):
            for other_entity in entities[i + 1:]:
                Physics.apply_gravity(entity, other_entity)


class MoveGroup(PhysicsGroup):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def update(self, delta_time: float):
        entities = [sprite.entity for sprite in self.sprites()]
        for entity in entities:
            Physics.move(entity, delta_time)


class SmartGroup(PhysicsGroup):
    def __init__(self, *sprites: SimRocketObject):
        super().__init__(*sprites)
        self.time = 0

    def update(self, delta_time: float):
        self.time += delta_time
        rockets = [sprite.entity for sprite in self.sprites()]
        for rocket in rockets:
            rocket.make_decision(delta_time)
            EventRegistrer.register_event(RocketEvent(self.time, rocket.speed.copy(), rocket.position))


class CollisionGroup(PhysicsGroup):
    def __init__(self, *sprites):
        super().__init__(*sprites)
        self.time = 0

    def update(self, delta_time: float):
        rockets = [sprite for sprite in self.sprites() if isinstance(sprite, SimRocketObject)]
        planets = [sprite for sprite in self.sprites() if isinstance(sprite, SimPlanetaryObject)]
        self.time += delta_time

        for rocket in rockets:
            for planet in planets:
                if Physics.calculate_distance(planet.entity.position, rocket.entity.position) < planet.entity.radius:
                    landing_angle_absolute = Vector(planet.entity.position, rocket.entity.position).polar_angle
                    landing_angle_relative = (landing_angle_absolute - planet.entity.polar_angle) % (2 * math.pi)
                    finite_speed_magnitude = (rocket.entity.speed - planet.entity.speed - planet.entity.surface_speed(landing_angle_absolute)).magnitude
                    EventRegistrer.register_event(CollisionEvent(self.time, planet, rocket, landing_angle_relative, finite_speed_magnitude))
                    rocket.kill()


class RotatingGroup(PhysicsGroup):
    def __init__(self, *sprites: SimPlanetaryObject):
        super().__init__(*sprites)

    def update(self, delta_time: float):
        planets = [sprite.entity for sprite in self.sprites()]

        for planet in planets:
            planet.polar_angle = (planet.polar_angle + delta_time * planet.angle_speed) % (pi * 2)


class RenderGroup(Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)
        pygame.font.init()
        self.font = pygame.font.Font(config.FONT_PATH, config.FONT_SIZE)

    def render(self, screen, scale: float, offset: Vector):
        for entity in self.sprites():
            entity.draw(screen, scale, offset, self.font)


class WidgetGroup(Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)
        pygame.font.init()
        self.font = pygame.font.Font(config.FONT_PATH, config.FONT_SIZE)

    def render(self, screen, time: float):
        if config.draw_widgets:
            for widget in self.sprites():
                widget.render(screen, self.font, time)
