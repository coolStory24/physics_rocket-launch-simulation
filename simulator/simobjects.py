import pygame
from pygame.sprite import Sprite

from config import MIN_PLANETARY_SIZE, ROCKET_MARKER_SIZE
from entities import Planet, BaseRocket
from physics import Entity, Vector


class SimObject(Sprite):
    def __init__(self, entity: Entity, color=pygame.Color("White"), name: str = ""):
        super().__init__()
        self.entity = entity
        self.name = name
        self.color = color

    def get_centre_on_screen(self, scale: float, offset: Vector):
        return (self.entity.position.x * scale + offset.x,
                self.entity.position.y * scale + offset.y)

    def draw_text_marker(self, screen, scale: float, offset: Vector, font, marker_vertical_offset: float = 0):
        text = font.render(self.name, True, self.color)
        text_size = text.get_width()
        x, y = self.get_centre_on_screen(scale, offset)
        screen.blit(text, (x - text.get_width() / 2, y -
                    marker_vertical_offset - text.get_height()))

    def draw(self, screen, scale: float, offset: Vector):
        raise NotImplementedError()


class SimPlanetaryObject(SimObject):
    def __init__(self, entity: Planet, color=pygame.Color("White"), name: str = "PLANET"):
        super().__init__(entity, color=color, name=name)

    def draw(self, screen, scale: float, offset: Vector, font, draw_marker: bool = True):
        if not isinstance(self.entity, Planet):
            raise ValueError("Entity is not a Planet")
        pygame.draw.circle(
            screen, self.color, self.get_centre_on_screen(scale, offset),
            max(int(self.entity.radius * scale), MIN_PLANETARY_SIZE)
        )

        if draw_marker:
            self.draw_text_marker(screen, scale, offset, font,
                                  self.entity.radius * scale)


class SimRocketObject(SimObject):
    def __init__(self, entity: BaseRocket, color=pygame.Color("firebrick1"), name: str = "ROCKET"):
        super().__init__(entity, color=color, name=name)

    def draw(self, screen, scale: float, offset: Vector, font, draw_marker: bool = True):
        if not isinstance(self.entity, BaseRocket):
            raise ValueError("Entity is not a Round Rocket")
        pygame.draw.circle(
            screen, self.color, self.get_centre_on_screen(scale, offset),
            ROCKET_MARKER_SIZE
        )

        if draw_marker:
            self.draw_text_marker(screen, scale, offset, font)
