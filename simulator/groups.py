import pygame
import math

from pygame.sprite import Group, Sprite
from math import pi

import config
from physics import Vector, Point, Physics
from entities import Planet, BaseRocket
from simobjects import SimRocketObject, SimPlanetaryObject
from events import RocketEvent, EventRegistrer, CollisionEvent
from events import GravityTrackingEvent


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
            EventRegistrer.register_event(RocketEvent(self.time, rocket.speed.copy(), rocket.position, rocket.planet.position))
            EventRegistrer.register_event(GravityTrackingEvent(self.time, rocket))


class CollisionGroup(PhysicsGroup):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def update(self, delta_time: float):
        rockets = [sprite for sprite in self.sprites() if isinstance(sprite, SimRocketObject)]
        planets = [sprite for sprite in self.sprites() if isinstance(sprite, SimPlanetaryObject)]

        for rocket in rockets:
            for planet in planets:
                if Physics.calculate_distance(planet.entity.position, rocket.entity.position) < planet.entity.radius:
                    landing_angle_absolute = Vector(planet.entity.position, rocket.entity.position).polar_angle
                    landing_angle_relative = (landing_angle_absolute - planet.entity.polar_angle) % (2 * math.pi)
                    finite_speed_magnitude = (rocket.entity.speed - planet.entity.speed - planet.entity.surface_speed(landing_angle_absolute)).magnitude
                    EventRegistrer.register_event(CollisionEvent(planet, rocket, landing_angle_relative, finite_speed_magnitude))
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

    def update_screen_settings(self, scale, offset: Vector):
        for sprite in self.sprites():
            sprite.update_screen_settings(scale, offset)

    def render(self, screen):
        for sprite in self.sprites():
            sprite.draw(screen, self.font)

        if config.draw_markers:
            for sprite in self.sprites():
                sprite.draw_text_marker(screen, self.font)


class WidgetGroup(Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)
        pygame.font.init()
        self.font = pygame.font.Font(config.FONT_PATH, config.FONT_SIZE)

    def render(self, screen, time: float):
        if config.draw_widgets:
            for widget in self.sprites():
                widget.render(screen, self.font, time)


class ClickableGroup(Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def process_mouseclick(self, mousepos: Point):
        for sprite in self.sprites():
            sprite.process_mouseclick(mousepos)


def create_physics_groups(*sprites):
    planets = [sprite for sprite in sprites if isinstance(sprite.entity, Planet)]
    rockets = [sprite for sprite in sprites if isinstance(sprite.entity, BaseRocket)]
    return (
        PhysicsGroup(*sprites),
        GravityGroup(*sprites),
        SmartGroup(*rockets),
        CollisionGroup(*sprites),
        RotatingGroup(*planets),
        MoveGroup(*sprites),
    )
