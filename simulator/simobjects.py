import pygame
from pygame.sprite import Sprite

import config
from entities import Planet, BaseRocket
from physics import Entity, Vector, Point
from events import EventRegistrer, FollowEventCapture


class SimObject(Sprite):
    def __init__(self, entity: Entity, color=pygame.Color("White"), name: str = ""):
        super().__init__()
        self.entity = entity
        self.name = name
        self.color = color

    @property
    def center_on_screen(self):
        return (self.entity.position.x * self.scale + self.offset.x,
                self.entity.position.y * self.scale + self.offset.y)

    def process_mouseclick(self, mousepos: Point):
        x, y = self.center_on_screen
        if max([abs(mousepos.x - x), abs(mousepos.y - y)]) < config.CLICK_RADIUS:
            EventRegistrer.register_event(FollowEventCapture(self, Vector(self.center_on_screen)))

    def update_screen_settings(self, scale: float, offset: Vector):
        self.scale = scale
        self.offset = offset

    def _draw_text_marker(self, screen, font, marker_vertical_offset: float = 0):
        text = font.render(self.name, True, self.color)
        x, y = self.center_on_screen
        screen.blit(text, (x - text.get_width() / 2, y -
                    marker_vertical_offset - text.get_height()))

    def draw_text_marker(self, screen, font):
        self._draw_text_marker(screen, font, 0)

    def draw(self, screen, font):
        raise NotImplementedError()


class SimPlanetaryObject(SimObject):
    def __init__(self, entity: Planet, color=pygame.Color("White"), name: str = "PLANET"):
        super().__init__(entity, color=color, name=name)

    def process_mouseclick(self, mousepos: Point):
        x, y = self.center_on_screen
        if max([abs(mousepos.x - x), abs(mousepos.y - y)]) < max([config.CLICK_RADIUS, self.entity.radius * self.scale]):
            EventRegistrer.register_event(FollowEventCapture(self, Vector(self.center_on_screen)))

    def draw(self, screen, font):
        if not isinstance(self.entity, Planet):
            raise ValueError("Entity is not a Planet")
        pygame.draw.circle(
            screen, self.color, self.center_on_screen,
            max(int(self.entity.radius * self.scale), config.MIN_PLANETARY_SIZE)
        )

    def draw_text_marker(self, screen, font):
        self._draw_text_marker(screen, font, self.entity.radius * self.scale)


class SimRocketObject(SimObject):
    def __init__(self, entity: BaseRocket, color=pygame.Color("firebrick1"), name: str = "ROCKET"):
        super().__init__(entity, color=color, name=name)

    def draw(self, screen, font):
        if not isinstance(self.entity, BaseRocket):
            raise ValueError("Entity is not a Rocket")
        pygame.draw.circle(
            screen, self.color, self.center_on_screen,
            config.ROCKET_MARKER_SIZE
        )
