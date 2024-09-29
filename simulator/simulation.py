import sys
import pygame
import time

import config
from groups import RenderGroup, WidgetGroup, ClickableGroup
from physics import Vector, Point
from config import MOUSE_SCALE_DELTA, OFFSET_DELTA, SCALE_DELTA
from events import Event, EventRegistrer, EventSubscriber, BuildPlotsEvent, PauseEvent, TimeScaleUpdateEvent, CaptureEvent
from widgets import LoggerWidget, ClockWidget, TimeScaleWidget
from logger import ConsoleLogger


class Simulation(EventSubscriber):
    def __init__(self, dimensions=(1920, 1080), offset = (960, 540), pixels_per_meter: float = 1E-5,
                 time_scale: float = 1E3, amount_of_iterations: float = 40, groups=(), widgets=(), clickable=()):
        self.width, self.height = dimensions
        self.main_window = None
        self.paused = False
        self.dragging = False
        self.pixels_per_meter = pixels_per_meter
        self.time_scale = time_scale
        self.amount_of_iterations = amount_of_iterations
        self.total_sim_time = 0
        self.offset = Vector(offset)
        self.mouse_on_time = 0

        self.objects = {sprite for group in groups for sprite in group}
        self.groups = groups
        self.render_group = RenderGroup(*self.objects)
        self.widget_group = WidgetGroup(widgets)
        self.clickable_group = ClickableGroup(clickable)

        self.followed_sprite = None

        if config.VERBOSE:
            self.console_logger = ConsoleLogger()

        self.subscribe(PauseEvent)
        self.subscribe(TimeScaleUpdateEvent)
        self.subscribe(CaptureEvent)

    @property
    def display_center(self):
        return Vector((pygame.display.Info().current_w / 2, pygame.display.Info().current_h / 2))

    def update_pixels_per_meter(self, center: Vector, delta: float):
        # recalculating offset to keep center in the same position on the screen
        self.offset = center - (center - self.offset) * delta

        self.pixels_per_meter *= delta

    def handle_event(self, event):
        if isinstance(event, PauseEvent):
            self.paused = not self.paused
        elif isinstance(event, TimeScaleUpdateEvent):
            self.time_scale = event.time_scale
            self.amount_of_iterations = event.amount_of_iterations
        elif isinstance(event, CaptureEvent):
            self.followed_sprite = event.captured_sprite

    def handle_pygame_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.update_pixels_per_meter(Vector((mouse_x, mouse_y)), MOUSE_SCALE_DELTA ** event.y if event.y > 0 else 1 / MOUSE_SCALE_DELTA ** (-event.y))

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.dragging = True
            self.mouse_on_time = time.time()
            pygame.mouse.get_rel()
            EventRegistrer.register_event(CaptureEvent(None))

        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            EventRegistrer.register_event(CaptureEvent(None))

            if time.time() - self.mouse_on_time < config.MOUSECLICK_TIME:
                self.clickable_group.process_mouseclick(Point(pygame.mouse.get_pos()))

        if event.type == pygame.MOUSEMOTION and self.dragging:
            self.offset += Vector(pygame.mouse.get_rel())

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                config.draw_markers = not config.draw_markers
            if event.key == pygame.K_h:
                config.draw_widgets = not config.draw_widgets
            if event.key == pygame.K_u:
                EventRegistrer.register_event(CaptureEvent(None))

            if event.key == pygame.K_p:
                EventRegistrer.register_event(BuildPlotsEvent())
            if event.key == pygame.K_SPACE:
                EventRegistrer.register_event(PauseEvent(not self.paused))
            if event.key == pygame.K_LEFTBRACKET and self.amount_of_iterations // config.AMOUNT_OF_ITERATIONS_DELTA >= 1:
                EventRegistrer.register_event(TimeScaleUpdateEvent(self.time_scale, self.amount_of_iterations // config.AMOUNT_OF_ITERATIONS_DELTA))
            if event.key == pygame.K_RIGHTBRACKET and self.amount_of_iterations * config.AMOUNT_OF_ITERATIONS_DELTA <= config.MAX_AMOUNT_OF_ITERATIONS:
                EventRegistrer.register_event(TimeScaleUpdateEvent(self.time_scale, self.amount_of_iterations * config.AMOUNT_OF_ITERATIONS_DELTA))

        # window is resized
        if event.type == pygame.VIDEORESIZE:
            self.width, self.height = event.w, event.h

    def process_keyboard(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            self.update_pixels_per_meter(self.display_center, SCALE_DELTA)
        if keys[pygame.K_MINUS]:
            self.update_pixels_per_meter(self.display_center, 1/SCALE_DELTA)

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.offset += Vector((0, OFFSET_DELTA))
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.offset += Vector((0, -OFFSET_DELTA))
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.offset += Vector((OFFSET_DELTA, 0))
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.offset += Vector((-OFFSET_DELTA, 0))

    def run(self):
        pygame.init()
        self.main_window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption('Rocket Simulator')
        icon = pygame.image.load(config.ICON_PATH)
        pygame.display.set_icon(icon)
        delta_time = 1 / 60
        clock = pygame.time.Clock()

        while True:
            self.main_window.fill(pygame.Color("black"))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    self.handle_pygame_event(event)

            self.process_keyboard()

            if not self.paused:
                for _ in range(self.amount_of_iterations):
                    for group in self.groups:
                        group.update(delta_time * self.time_scale)

                    self.total_sim_time += delta_time * self.time_scale

            if self.followed_sprite is not None:
                self.offset += self.display_center - Vector(self.followed_sprite.centre_on_screen)

            self.render_group.update_screen_settings(self.pixels_per_meter, self.offset)
            self.render_group.render(self.main_window)
            self.widget_group.render(self.main_window, self.total_sim_time)

            pygame.display.flip()
            clock.tick(60)
