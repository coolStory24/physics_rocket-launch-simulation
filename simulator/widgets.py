from pygame.sprite import Sprite
import pygame

import config
from logger import Logger
from events import EventSubscriber, PauseEvent, TimeScaleUpdateEvent, FollowEvent, FollowEventCapture, FollowEventUncapture, SetSimulationTimeScaleEvent


class Widget(Sprite):
    def __init__(self):
        super().__init__()

    def render(self, screen, font, simtime: float):
        raise NotImplementedError()


class LoggerWidget(Widget, Logger):
    def __init__(self):
        self.event_strings = []
        Widget.__init__(self)
        Logger.__init__(self)

    def handle_event(self, event):
        event_string = str(event)
        self.event_strings.append(event_string)

    def render(self, screen, font, simtime: float):
        event_texts = [font.render(text, True, "White") for text in self.event_strings]
        x = screen.get_width() - config.WIDGET_MARGIN
        y = screen.get_height() - config.WIDGET_MARGIN

        for text in reversed(event_texts):
            screen.blit(text, (x - text.get_width(), y - text.get_height()))
            y -= text.get_height()


class ClockWidget(Widget):
    def __init__(self):
        super().__init__()

    def render(self, screen, font, simtime):
        minutes = int(simtime // 60 % 60)
        hours = int(simtime // 3600 % 24)
        days = int(simtime // 3600 // 24)
        to_print = f"Time: {days} days {"0" if hours < 10 else ""}{hours}h {"0" if minutes < 10 else ""}{minutes}m"
        text = font.render(to_print, True, "White")
        screen.blit(text, (screen.get_width() - text.get_width() - config.WIDGET_MARGIN, config.WIDGET_MARGIN))


class TimeScaleWidget(Widget, EventSubscriber):
    def __init__(self, is_paused, time_scale, amount_of_iterations):
        super().__init__()
        self.is_paused = is_paused
        self.time_scale = time_scale
        self.amount_of_iterations = amount_of_iterations
        self.subscribe(PauseEvent, TimeScaleUpdateEvent, SetSimulationTimeScaleEvent)

    def handle_event(self, event):
        if isinstance(event, PauseEvent):
            self.is_paused = event.is_paused
        elif isinstance(event, TimeScaleUpdateEvent):
            self.time_scale = event.time_scale
            self.amount_of_iterations = event.amount_of_iterations
        elif isinstance(event, SetSimulationTimeScaleEvent):
            self.time_scale = event.time_scale
        else:
            raise ValueError("Unsupported event")

    def render(self, screen, font, simtime):
        if self.is_paused:
            text = font.render("Paused!", True, "White")
        else:
            text = font.render(f"X{int(self.time_scale * self.amount_of_iterations)}", True, "White")
        screen.blit(text, (config.WIDGET_MARGIN, config.WIDGET_MARGIN))


class CaptureWidget(Widget, EventSubscriber):
    def __init__(self, followed_sprite):
        super().__init__()
        self.subscribe(FollowEvent)
        self.followed_sprite = followed_sprite

    def handle_event(self, event):
        if isinstance(event, FollowEventCapture):
            self.followed_sprite = event.captured_sprite
        else:
            self.followed_sprite = None

    def render(self, screen, font, simtime):
        if self.followed_sprite is None:
            return

        text = font.render(f"{self.followed_sprite.name} is captured (escape to uncapture)", True, self.followed_sprite.color)
        screen.blit(text, (config.WIDGET_MARGIN, screen.get_height() - text.get_height() - config.WIDGET_MARGIN))
