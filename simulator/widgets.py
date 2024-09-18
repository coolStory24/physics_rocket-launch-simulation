from pygame.sprite import Sprite

import events
from logger import Logger
from config import WIDGET_MARGIN


class Widget(Sprite):
    def __init__(self):
        super().__init__()

    def render(self, screen, font, simtime: float):
        raise NotImplementedError()


class LoggerWidget(Widget, Logger):
    def __init__(self):
        Widget.__init__(self)
        Logger.__init__(self)
        self.event_strings = []

    def handle_event(self, event):
        event_string = str(event)
        self.event_strings.append(event_string)

    def render(self, screen, font, simtime: float):
        event_texts = [font.render(text, True, "White") for text in self.event_strings]
        x = screen.get_width() - WIDGET_MARGIN
        y = screen.get_height() - WIDGET_MARGIN

        for text in reversed(event_texts):
            screen.blit(text, (x - text.get_width(), y - text.get_height()))
            y -= text.get_height()


class ClockWidget(Widget):
    def __init__(self):
        super().__init__()

    def render(self, screen, font, simtime):
        seconds = int(simtime % 60)
        minutes = int(simtime // 60 % 60)
        hours = int(simtime // 3600 % 24)
        days = int(simtime // 3600 // 24)
        to_print = f"Time passed since simulation start: {days} days {hours}h {"0" if minutes < 10 else ""}{minutes}m"
        text = font.render(to_print, True, "White")
        screen.blit(text, (screen.get_width() - text.get_width() - WIDGET_MARGIN, WIDGET_MARGIN))
