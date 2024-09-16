import sys

import pygame

from groups import RenderGroup, PhysicsGroup
from physics import Vector
from config import MOUSE_SCALE_DELTA, OFFSET_DELTA, SCALE_DELTA

class Simulation:
    def __init__(self, dimensions=(1280, 720), offset = (640, 360), pixels_per_meter: float = 1E-6, time_scale: float = 1E5, groups=()):
        self.width, self.height = dimensions
        self.main_window = None
        self.paused = False
        self.dragging = False
        self.pixels_per_meter = pixels_per_meter
        self.time_scale = time_scale

        self.objects = {sprite for group in groups for sprite in group}

        self.groups = [PhysicsGroup(*self.objects)] + list(groups[::])
        self.render_group = RenderGroup(*self.objects)

        self.offset = Vector(offset)

    def handle_event(self, event):
        # change scale with mouse wheel
        if event.type == pygame.MOUSEWHEEL and self.pixels_per_meter + event.y * MOUSE_SCALE_DELTA > 0:
            self.pixels_per_meter += event.y * MOUSE_SCALE_DELTA

        # hold any mouse button to drag
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.dragging = True
            pygame.mouse.get_rel()
        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        if event.type == pygame.MOUSEMOTION and self.dragging:
            self.offset += Vector(pygame.mouse.get_rel())

        # window is resized
        if event.type == pygame.VIDEORESIZE:
            self.width, self.height = event.w, event.h

    def process_keyboard(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            self.pixels_per_meter += SCALE_DELTA
        if keys[pygame.K_MINUS] and self.pixels_per_meter - SCALE_DELTA > 0:
            self.pixels_per_meter -= SCALE_DELTA

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
        delta_time = 0.016
        clock = pygame.time.Clock()

        while not self.paused:
            self.main_window.fill(pygame.Color("black"))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    self.handle_event(event)

            self.process_keyboard()

            for group in self.groups:
                group.update(delta_time * self.time_scale)
                self.render_group.render(self.main_window, self.pixels_per_meter, self.offset)

            pygame.display.flip()
            delta_time = clock.tick(60) / 1000
