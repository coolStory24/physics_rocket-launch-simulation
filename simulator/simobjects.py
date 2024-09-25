import pygame
import math
from pygame.sprite import Sprite

import config
from entities import Planet, BaseRocket, Orbit
from physics import Entity, Vector, Point


class SimObject(Sprite):
    def __init__(self, entity: Entity, color=pygame.Color("White"), name: str = ""):
        super().__init__()
        self.entity = entity
        self.name = name
        self.color = color

    @staticmethod
    def to_screen_position(point: Point, scale: float, offset: Vector):
        return (point.x * scale + offset.x,
                point.y * scale + offset.y)

    def get_centre_on_screen(self, scale: float, offset: Vector):
        return SimObject.to_screen_position(self.entity.position, scale, offset)

    def _draw_text_marker(self, screen, scale: float, offset: Vector, font, marker_vertical_offset: float = 0):
        text = font.render(self.name, True, self.color)
        x, y = self.get_centre_on_screen(scale, offset)
        screen.blit(text, (x - text.get_width() / 2, y -
                    marker_vertical_offset - text.get_height()))

    def draw_text_marker(self, screen, scale: float, offset: Vector, font):
        self._draw_text_marker(screen, scale, offset, font, 0)

    def draw(self, screen, scale: float, offset: Vector, font):
        raise NotImplementedError()


class SimPlanetaryObject(SimObject):
    def __init__(self, entity: Planet, color=pygame.Color("White"), name: str = "PLANET"):
        super().__init__(entity, color=color, name=name)

    def draw(self, screen, scale: float, offset: Vector, font):
        if not isinstance(self.entity, Planet):
            raise ValueError("Entity is not a Planet")
        pygame.draw.circle(
            screen, self.color, self.get_centre_on_screen(scale, offset),
            max(int(self.entity.radius * scale), config.MIN_PLANETARY_SIZE)
        )
        pygame.draw.circle(
            screen, "firebrick1", self.get_centre_on_screen(scale, offset), 1
        )

    def draw_text_marker(self, screen, scale: float, offset: Vector, font):
        self._draw_text_marker(screen, scale, offset, font, self.entity.radius * scale)


class SimRocketObject(SimObject):
    def __init__(self, entity: BaseRocket, color=pygame.Color("firebrick1"), name: str = "ROCKET"):
        super().__init__(entity, color=color, name=name)

    def draw(self, screen, scale: float, offset: Vector, font):
        if not isinstance(self.entity, BaseRocket):
            raise ValueError("Entity is not a Rocket")
        pygame.draw.circle(
            screen, self.color, self.get_centre_on_screen(scale, offset),
            config.ROCKET_MARKER_SIZE
        )

    # @staticmethod
    # def draw_ellipse_angle(surface, color, rect, angle, width=0, offset):
    #     target_rect = pygame.Rect(rect)
    #     shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    #     pygame.draw.ellipse(shape_surf, color, (0, 0, *target_rect.size), width)
    #     rotated_surf = pygame.transform.rotate(shape_surf, angle)
    #     surface.blit(rotated_surf, rotated_surf.get_rect(center = target_rect.center))


    def draw_orbit(self, screen, scale: float, offset: Vector):
        orbit = Orbit.calculate_orbit(self.entity.planet, self.entity)
        centre = self.entity.planet.position
        rect = pygame.Rect(
                offset.x + (centre.x - orbit.perigee_distance) * scale,
                offset.y + (centre.y - orbit.semi_minor_axis) * scale,
                (orbit.perigee_distance + orbit.apogee_distance) * scale,
                2 * orbit.semi_minor_axis * scale
        )
        target_rect = pygame.Rect(rect)
        polar_angle = Vector(self.entity.position, self.entity.planet.position).polar_angle
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.ellipse(shape_surf, "firebrick1", (0, 0, *target_rect.size), 1)
        print(orbit.polar_angle, polar_angle, self.entity.get_height(), orbit.apogee_height)
        rotated_surf = pygame.transform.rotate(shape_surf, 180 * (orbit.polar_angle + math.pi) / math.pi)
        # offset_addition = Vector.make_vector_by_polar_angle(orbit.polar_angle, orbit.eccentricity * orbit.semi_major_axis * scale)
        offset_addition = Vector((1, 0)).rotate(math.pi - orbit.polar_angle) * orbit.eccentricity * orbit.semi_major_axis
        screen.blit(rotated_surf,
                    rotated_surf.get_rect(center = SimObject.to_screen_position(
                            self.entity.planet.position + offset_addition
                            , scale, offset
                        )
                                          # SimObject.to_screen_position(
            # self.entity.position - Vector.make_vector_by_polar_angle(orbit.polar_angle, orbit.eccentricity * orbit.semi_major_axis), scale, offset))
        ))
